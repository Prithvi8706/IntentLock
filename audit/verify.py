import argparse

from audit.ledger import verify_chain


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify the Decision Guard ledger hash chain")
    parser.add_argument("path", nargs="?", default="audit/ledger.jsonl")
    args = parser.parse_args()
    valid, index, event_type = verify_chain(args.path)
    if valid:
        print("Ledger verified")
        return 0
    print(f"Ledger broken at event {index} ({event_type})")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

