from decimal import Decimal, InvalidOperation


def moeda_para_centavos(valor_str):
    if not valor_str:
        return 0
    try:
        limpo = valor_str.replace("R$", "").replace(" ", "").replace(".", "").replace(",", ".")
        val = Decimal(limpo)
        return float(val)
    except (InvalidOperation, ValueError):
        return 0.0


def centavos_para_moeda(valor):
    if valor is None:
        return "R$ 0,00"
    if isinstance(valor, (int, float, Decimal)):
        return f"R$ {valor:.2f}".replace(".", ",")
    return str(valor)
