#!/usr/bin/env python3
"""Build a normalized wallet risk dataset from Data2.txt."""
from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set

ROOT = Path(__file__).resolve().parent.parent
INPUT_PATH = ROOT / "Data2.txt"
OUTPUT_PATH = ROOT / "app" / "repositories" / "data" / "wallet_risk_dataset.json"

CATEGORY_RISK_MAP = {
    "CONTRACT_EXPLOIT": "CRÍTICO",
    "OTHER_HACK": "CRÍTICO",
    "RUG_PULL": "CRÍTICO",
    "HACK": "CRÍTICO",
    "PIGBUTCHERING": "ALTO",
    "PIG_BUTCHERING": "ALTO",
    "PHISHING": "ALTO",
    "SEXTORTION": "ALTO",
    "DONATION_SCAM": "MEDIO",
    "FAKE_PROJECT": "MEDIO",
    "ROMANCE": "MEDIO",
    "IMPERSONATION": "MEDIO",
    "FAKE_RETURNS": "MEDIO",
    "AIRDROP": "BAJO",
    "OTHER": "MEDIO",
}

RISK_ORDER = {
    None: -1,
    "BAJO": 0,
    "MEDIO": 1,
    "ALTO": 2,
    "CRÍTICO": 3,
}


def normalize_risk_level(level: Optional[str]) -> Optional[str]:
    if not level:
        return None
    level = level.strip().upper()
    replacements = {
        "CRITICO": "CRÍTICO",
        "CRITICAL": "CRÍTICO",
        "ALTA": "ALTO",
        "MEDIA": "MEDIO",
        "BAJA": "BAJO",
    }
    level = replacements.get(level, level)
    if level not in {"BAJO", "MEDIO", "ALTO", "CRÍTICO"}:
        return None
    return level


def guess_network(address: str) -> Optional[str]:
    if not address:
        return None
    addr = address.strip()
    if addr.startswith("0x"):
        return "EVM"
    if addr.startswith("bc1") or addr.startswith("1") or addr.startswith("3"):
        return "BTC"
    if addr.startswith("3") and len(addr) > 30:
        return "BTC"
    if addr.startswith("tb1"):
        return "BTC"
    if addr.startswith("T") and len(addr) in {33, 34}:
        return "TRON"
    if addr.upper().startswith("TRON"):
        return "TRON"
    if addr.startswith("4") and len(addr) == 34:
        return "TRON"
    if addr.startswith("L") and len(addr) >= 26:
        return "LITECOIN"
    if addr.lower().startswith("addr1"):
        return "CARDANO"
    if addr.upper().startswith("IA") and len(addr) > 40:
        return "ALGORAND"
    if addr.upper().startswith("C") and len(addr) > 40:
        return "SOL"
    return None


def extract_json_objects(raw_text: str) -> List[Any]:
    objects: List[Any] = []
    decoder = json.JSONDecoder()
    idx = raw_text.find("{")
    if idx == -1:
        return objects
    while idx < len(raw_text):
        try:
            obj, end = decoder.raw_decode(raw_text, idx)
        except json.JSONDecodeError:
            break
        objects.append(obj)
        idx = end
        while idx < len(raw_text) and raw_text[idx].isspace():
            idx += 1
    return objects


def add_source(wallet: Dict[str, Any], source_entry: Dict[str, Any]) -> None:
    key = (
        source_entry.get("source"),
        source_entry.get("detail"),
        source_entry.get("risk_level"),
        source_entry.get("scam_category"),
        source_entry.get("createdAt"),
    )
    if key in wallet["_source_keys"]:
        return
    wallet["_source_keys"].add(key)
    wallet["sources"].append({k: v for k, v in source_entry.items() if v is not None})


def ensure_wallet(registry: Dict[str, Dict[str, Any]], address: str) -> Dict[str, Any]:
    if address not in registry:
        registry[address] = {
            "address": address,
            "networks": set(),
            "risk_levels": set(),
            "risk_score": None,
            "scam_categories": set(),
            "domains": set(),
            "sources": [],
            "_source_keys": set(),
        }
    return registry[address]


def parse_category_tokens(text: str) -> Set[str]:
    if not text:
        return set()
    tokens: Set[str] = set()
    upper_text = text.upper()
    for category in CATEGORY_RISK_MAP.keys():
        if category in upper_text:
            tokens.add(category)
    pattern_tokens = set(re.findall(r"[A-Z][A-Z_]+", upper_text))
    tokens.update(tok for tok in pattern_tokens if "_" in tok)
    return tokens


def process_dataset(objects: List[Any]) -> Dict[str, Any]:
    wallets: Dict[str, Dict[str, Any]] = {}
    metadata: Dict[str, Any] = {}
    reports_container: Dict[str, Any] = {}
    standalone_reports: List[Dict[str, Any]] = []

    if objects:
        metadata = objects[0]
    if len(objects) >= 2 and isinstance(objects[1], dict) and "reports" in objects[1]:
        reports_container = objects[1]
        standalone_reports = [obj for obj in objects[2:] if isinstance(obj, dict) and "addresses" in obj]
    elif len(objects) > 1:
        standalone_reports = [obj for obj in objects[1:] if isinstance(obj, dict) and "addresses" in obj]

    # Process OFAC sanctions
    ofac = metadata.get("data_sources", {}).get("ofac_sanctions", {})
    for address, detail in ofac.get("addresses", {}).items():
        wallet = ensure_wallet(wallets, address)
        network = None
        match = re.search(r"\(([^)]+)\)", detail)
        if match:
            network = match.group(1).strip().upper()
        if network:
            wallet["networks"].add(network)
        risk_level = normalize_risk_level(detail.split("-", 1)[0])
        if risk_level:
            wallet["risk_levels"].add(risk_level)
        wallet["scam_categories"].add("SANCTION")
        add_source(
            wallet,
            {
                "source": "OFAC Sanctions (Simulado)",
                "type": ofac.get("type"),
                "detail": detail,
                "risk_level": risk_level,
            },
        )

    # Process TRM risk scores
    trm = metadata.get("data_sources", {}).get("trm_risk_scores", {})
    for address, score in trm.get("scores", {}).items():
        wallet = ensure_wallet(wallets, address)
        wallet["risk_score"] = max(score, wallet["risk_score"]) if wallet["risk_score"] is not None else score
        if score >= 0.9:
            risk_level = "ALTO"
        elif score >= 0.4:
            risk_level = "MEDIO"
        else:
            risk_level = "BAJO"
        wallet["risk_levels"].add(risk_level)
        network = guess_network(address)
        if network:
            wallet["networks"].add(network)
        add_source(
            wallet,
            {
                "source": "TRM Labs (Simulado)",
                "type": trm.get("type"),
                "risk_level": risk_level,
                "score": score,
            },
        )

    # Process Chainabuse individual address risks
    chainabuse = metadata.get("data_sources", {}).get("chainabuse_reports", {})
    for address, detail in chainabuse.get("individual_addresses_risk", {}).items():
        wallet = ensure_wallet(wallets, address)
        parts = detail.split("-", 1)
        risk_level = normalize_risk_level(parts[0] if parts else None)
        if risk_level:
            wallet["risk_levels"].add(risk_level)
        tokens = parse_category_tokens(detail)
        wallet["scam_categories"].update(tokens)
        match = re.search(r"\(([^)]+)\)", detail)
        network = match.group(1).strip().upper() if match else guess_network(address)
        if network:
            wallet["networks"].add(network)
        add_source(
            wallet,
            {
                "source": "Chainabuse Individual Address Risk",
                "type": "COMMUNITY_REPORT",
                "detail": detail,
                "risk_level": risk_level,
                "scam_category": next(iter(tokens), None),
            },
        )

    # Process Chainabuse full hack reports
    for report in chainabuse.get("full_hack_reports", []) or []:
        risk_level = normalize_risk_level(report.get("risk_level"))
        scam_category = report.get("scamCategory")
        created_at = report.get("createdAt")
        for address in report.get("affected_wallets", []) or []:
            wallet = ensure_wallet(wallets, address)
            if risk_level:
                wallet["risk_levels"].add(risk_level)
            if scam_category:
                wallet["scam_categories"].add(scam_category)
            network = guess_network(address)
            if network:
                wallet["networks"].add(network)
            add_source(
                wallet,
                {
                    "source": "Chainabuse Full Hack Reports",
                    "type": "COMMUNITY_REPORT",
                    "risk_level": risk_level,
                    "scam_category": scam_category,
                    "detail": f"Hack report {report.get('id')}",
                    "createdAt": created_at,
                    "trusted": report.get("trusted"),
                },
            )

    # Process reports container
    def process_report(report: Dict[str, Any], source_name: str) -> None:
        scam_category = report.get("scamCategory")
        created_at = report.get("createdAt")
        trusted = report.get("trusted")
        addresses = report.get("addresses", []) or []
        domains = {item["domain"] for item in addresses if item.get("domain")}
        for item in addresses:
            address = item.get("address")
            if not address:
                continue
            wallet = ensure_wallet(wallets, address)
            chain = item.get("chain")
            if chain:
                wallet["networks"].add(chain.upper())
            else:
                network = guess_network(address)
                if network:
                    wallet["networks"].add(network)
            if scam_category:
                wallet["scam_categories"].add(scam_category)
                mapped_risk = normalize_risk_level(CATEGORY_RISK_MAP.get(scam_category))
                if mapped_risk:
                    wallet["risk_levels"].add(mapped_risk)
            wallet["domains"].update(domains)
            add_source(
                wallet,
                {
                    "source": source_name,
                    "type": "COMMUNITY_REPORT",
                    "risk_level": CATEGORY_RISK_MAP.get(scam_category),
                    "scam_category": scam_category,
                    "detail": f"Reporte {report.get('id')}",
                    "createdAt": created_at,
                    "trusted": trusted,
                },
            )

    for report in reports_container.get("reports", []) or []:
        process_report(report, "Chainabuse Reports Consolidated")

    for report in standalone_reports:
        process_report(report, "Chainabuse Reports Incremental")

    # Finalize wallet entries
    final_wallets: Dict[str, Any] = {}
    for address, data in wallets.items():
        risk_level = None
        if data["risk_levels"]:
            risk_level = max(data["risk_levels"], key=lambda level: RISK_ORDER.get(level, -1))
        risk_score = data["risk_score"]
        networks = sorted({net for net in data["networks"] if net})
        if not networks:
            networks = ["DESCONOCIDA"]
        scam_categories = sorted(data["scam_categories"])
        domains = sorted(data["domains"])
        dates = []
        for src in data["sources"]:
            created_at = src.get("createdAt")
            if created_at:
                try:
                    dates.append(datetime.fromisoformat(created_at.replace("Z", "+00:00")))
                except ValueError:
                    pass
        first_seen = min(dates).isoformat().replace("+00:00", "Z") if dates else None
        last_seen = max(dates).isoformat().replace("+00:00", "Z") if dates else None
        final_wallets[address] = {
            "networks": networks,
            "risk_level": risk_level,
            "risk_score": risk_score,
            "scam_categories": scam_categories,
            "domains": domains,
            "sources": data["sources"],
            "first_seen": first_seen,
            "last_seen": last_seen,
        }

    dataset_info = {
        "description": metadata.get("description"),
        "version": metadata.get("version"),
        "date_generated": metadata.get("date_generated"),
        "risk_categories": metadata.get("risk_categories"),
        "source_file": str(INPUT_PATH.name),
        "records": len(final_wallets),
        "extracted_at": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
    }

    return {
        "metadata": dataset_info,
        "wallets": final_wallets,
    }


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"No se encontró el archivo de entrada: {INPUT_PATH}")
    raw_text = INPUT_PATH.read_text(encoding="utf-8")
    objects = extract_json_objects(raw_text)
    dataset = process_dataset(objects)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(dataset, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Dataset generado en {OUTPUT_PATH} con {dataset['metadata']['records']} wallets")


if __name__ == "__main__":
    main()
