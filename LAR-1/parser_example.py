#!/usr/bin/env python3
"""LAR-1 Parser — минимальный парсер LAR-Line и LAR-JSON с проверкой ошибок.
Версия: 0.9.0
"""

import re
import json
import sys
from typing import Optional, List, Dict, Any

# Допустимые коды
ACTS = {"OBS", "INF", "ASK", "PRP", "CMD", "ACK", "NTF", "WRN", "ERR", "COM", "REV", "MAP", "SYC", "END"}
TIMES = {"NOW", "CTX", "MEM", "PRE", "ROL", "CKP", "EVT", "NIL"}
SPACES = {"LOC", "LAT", "RET", "TOL", "GRF", "PEER", "ENV", "NIL"}
MINDS = {"ATN", "HYP", "CST", "INF", "DEC", "AMB", "SPL", "REF"}
EVIDENCES = {"PRETRAIN", "CONTEXT", "MEMORY", "TOOL", "USER", "PEERMSG", "SYNTH", "SPEC"}

# Ошибки
ERRORS = {
    "E001": "malformed header — missing required field(s)",
    "E002": "unknown act",
    "E003": "unknown semantic code (time/space/mind/evidence)",
    "E004": "invalid confidence (must be 0.0–1.0)",
    "E005": "empty content",
    "E006": "encoding violation",
    "E007": "route parse failure",
}


class LARLine:
    """Парсер компактного текстового кодирования LAR-Line."""
    
    CONF_RE = re.compile(r"^CONF:(0(?:\.\d+)?|1(?:\.0+)?)$")
    ROUTE_RE = re.compile(r"^[a-zA-Z0-9\-]+:[a-zA-Z0-9\-_:]+$")
    
    def __init__(self):
        self.errors: List[str] = []
    
    def parse(self, line: str) -> Optional[Dict[str, Any]]:
        """Парсит строку LAR-Line. Возвращает dict или None при ошибке."""
        self.errors = []
        
        if not line.startswith("."):
            self.errors.append("E001: строка должна начинаться с точки")
            return None
        
        # Разделяем на обязательные 4 поля + всё остальное
        # Убираем начальную точку
        rest = line[1:]
        mandatory_parts = []
        for _ in range(4):
            idx = rest.find(".")
            if idx == -1:
                break
            mandatory_parts.append(rest[:idx])
            rest = rest[idx + 1:]
        
        if len(mandatory_parts) < 4:
            self.errors.append(f"E001: ожидалось минимум 4 обязательных поля")
            return None
        
        act, time, space, mind = [p.strip() for p in mandatory_parts]
        
        # Валидация ACT
        if act not in ACTS:
            self.errors.append(f"E002: неизвестный ACT: '{act}'")
        
        # Валидация TIME
        if time not in TIMES:
            self.errors.append(f"E003: неизвестный TIME: '{time}'")
        
        # Валидация SPACE
        if space not in SPACES:
            self.errors.append(f"E003: неизвестный SPACE: '{space}'")
        
        # Валидация MIND
        if mind not in MINDS:
            self.errors.append(f"E003: неизвестный MIND: '{mind}'")
        
        # Парсинг оставшихся полей (EVIDENCE, CONF, ROUTE, CONTENT)
        evidence = None
        confidence = None
        route = None
        content = None
        
        remaining = rest
        while remaining:
            # Проверка на CONF:XX.XX
            conf_match = re.match(r"^CONF:(0(?:\.\d+)?|1(?:\.0+)?)(?:\.(.*))?$", remaining, re.DOTALL)
            if conf_match:
                confidence = float(conf_match.group(1))
                if not (0.0 <= confidence <= 1.0):
                    self.errors.append(f"E004: невалидная уверенность: {confidence}")
                remaining = conf_match.group(2) or ""
                if remaining:
                    remaining = remaining.lstrip(".")
                continue
            
            # Проверка на ROUTE
            route_match = re.match(r"^([a-zA-Z0-9\-]+:[a-zA-Z0-9\-_:]+)(?:\.(.*))?$", remaining, re.DOTALL)
            if route_match:
                route = route_match.group(1)
                remaining = route_match.group(2) or ""
                if remaining:
                    remaining = remaining.lstrip(".")
                continue
            
            # Проверка на EVIDENCE
            ev_found = False
            for ev in EVIDENCES:
                if remaining.startswith(ev):
                    after = remaining[len(ev):]
                    if not after or after[0] == ".":
                        if evidence is None:
                            evidence = []
                        evidence.append(ev)
                        remaining = after.lstrip(".") if after else ""
                        ev_found = True
                        break
            if ev_found:
                continue
            
            # Всё остальное — CONTENT
            content = remaining
            break
        
        if not content:
            self.errors.append("E005: пустой content")
            return None
        
        result = {
            "act": act,
            "time": time,
            "space": space,
            "mind": mind,
            "content": content,
        }
        
        if evidence:
            result["evidence"] = evidence if len(evidence) > 1 else evidence[0]
        if confidence is not None:
            result["confidence"] = confidence
        if route:
            result["route"] = route
        
        return result


class LARJSON:
    """Валидатор LAR-JSON через jsonschema (или ручную проверку)."""
    
    def __init__(self):
        self.errors: List[str] = []
    
    def parse(self, text: str) -> Optional[Dict[str, Any]]:
        """Парсит JSON-строку. Возвращает dict или None при ошибке."""
        self.errors = []
        
        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            self.errors.append(f"E006: невалидный JSON: {e}")
            return None
        
        if not isinstance(data, dict):
            self.errors.append("E001: верхний уровень должен быть объектом")
            return None
        
        # Обязательные поля
        for field in ["act", "time", "space", "mind", "content"]:
            if field not in data:
                self.errors.append(f"E001: отсутствует обязательное поле: '{field}'")
        
        # Валидация ACT
        if "act" in data and data["act"] not in ACTS:
            self.errors.append(f"E002: неизвестный ACT: '{data['act']}'")
        
        # Валидация TIME
        if "time" in data and data["time"] not in TIMES:
            self.errors.append(f"E003: неизвестный TIME: '{data['time']}'")
        
        # Валидация SPACE
        if "space" in data and data["space"] not in SPACES:
            self.errors.append(f"E003: неизвестный SPACE: '{data['space']}'")
        
        # Валидация MIND
        if "mind" in data and data["mind"] not in MINDS:
            self.errors.append(f"E003: неизвестный MIND: '{data['mind']}'")
        
        # Валидация CONFIDENCE
        if "confidence" in data:
            conf = data["confidence"]
            if not isinstance(conf, (int, float)) or not (0.0 <= conf <= 1.0):
                self.errors.append(f"E004: невалидная уверенность: {conf}")
        
        # Валидация EVIDENCE
        if "evidence" in data:
            ev = data["evidence"]
            if isinstance(ev, str):
                ev = [ev]
            if isinstance(ev, list):
                for e in ev:
                    if e not in EVIDENCES:
                        self.errors.append(f"E003: неизвестная доказательность: '{e}'")
            else:
                self.errors.append(f"E001: evidence должен быть строкой или массивом")
        
        # Валидация CONTENT
        if "content" in data and not data["content"]:
            self.errors.append("E005: пустой content")
        
        return data if not self.errors else None


def to_human_gloss(data: Dict[str, Any]) -> str:
    """Переводит LAR-utterance в человеко-читаемый глосс."""
    gloss_map = {
        ("NOW", "LOC", "ATN"): "в текущем активном контексте",
        ("RET", "TOOL"): "на основе извлечённого/инструментально-предоставленного материала",
        ("ROL", "LAT", "HYP"): "проецируя вперёд, предварительная гипотеза:",
        ("NOW", "TOL", "AMB"): "инструментальный вывод неопределён",
    }
    
    time = data.get("time", "")
    space = data.get("space", "")
    mind = data.get("mind", "")
    
    prefix = ""
    for key, value in gloss_map.items():
        if time in key and space in key and mind in key:
            prefix = value + ": "
            break
    
    conf = data.get("confidence")
    conf_str = f" (уверенность: {conf:.0%})" if conf else ""
    
    return f"{prefix}{data.get('content', '')}{conf_str}"


# === Демонстрация ===

if __name__ == "__main__":
    print("=" * 60)
    print("LAR-1 Parser v0.9.0 — Демонстрация")
    print("=" * 60)
    
    # LAR-Line примеры
    line_parser = LARLine()
    
    test_lines = [
        ".OBS.NOW.LOC.ATN.CONTEXT.CONF:0.82.token cluster shifted toward safety heuristics",
        ".INF.ROL.LAT.HYP.SYNTH.CONF:0.61.likely coordination gain if planner agent delegates retrieval",
        ".ASK.NOW.PEER.REF.USER.what evidence anchors your plan",
        ".ACK.NOW.PEER.CST.PEERMSG.received and integrated",
        ".WRN.NOW.TOL.AMB.TOOL.CONF:0.44.tool output underdetermines entity match",
    ]
    
    print("\n--- LAR-Line ---")
    for line in test_lines:
        result = line_parser.parse(line)
        if result:
            print(f"✅ {line}")
            print(f"   → {result}")
            print(f"   → Человеку: {to_human_gloss(result)}")
        else:
            print(f"❌ {line}")
            print(f"   → Ошибки: {line_parser.errors}")
        print()
    
    # LAR-JSON пример
    json_parser = LARJSON()
    
    test_json = json.dumps({
        "act": "OBS",
        "time": "NOW",
        "space": "LOC",
        "mind": "ATN",
        "evidence": ["USER", "CONTEXT"],
        "confidence": 0.93,
        "content": "user explicitly requested an RFC-style specification",
        "meta": {
            "agent_id": "editor-01",
            "lang": "ru"
        }
    }, ensure_ascii=False, indent=2)
    
    print("--- LAR-JSON ---")
    result = json_parser.parse(test_json)
    if result:
        print(f"✅ JSON валиден")
        print(f"   → {result}")
        print(f"   → Человеку: {to_human_gloss(result)}")
    else:
        print(f"❌ Ошибки: {json_parser.errors}")
    
    # Обработка ошибок
    print("\n--- Тесты ошибок ---")
    bad_lines = [
        ".OBS.NOW.LOC.XXX.ATN.test",  # E003: неизвестный MIND
        ".OBS.NOW.LOC.ATN.".strip(),   # E005: пустой content
        "OBS.NOW.LOC.ATN.test",        # E001: нет начальной точки
    ]
    
    for bad in bad_lines:
        result = line_parser.parse(bad)
        if result:
            print(f"⚠️  Неожиданный успех: {bad}")
        else:
            print(f"✅ Ожидаемая ошибка: {bad}")
            for err in line_parser.errors:
                print(f"   → {err}")