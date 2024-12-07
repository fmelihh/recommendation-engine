import hashlib


class HashGenerator:
    @staticmethod
    def generate_unique_hash(args: list[str]) -> str:
        merged_values = "_".join(args)
        return hashlib.sha256(merged_values.encode("utf-8")).hexdigest()
