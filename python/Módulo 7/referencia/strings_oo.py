"""Referências de OO para os dois exercícios. Execute: python strings_oo.py."""

from dataclasses import dataclass


@dataclass(frozen=True)
class StringComparison:
    """Um objeto representa um par de strings, sem permitir sua substituição."""

    first: str
    second: str

    @property
    def same_content(self) -> bool:
        return self.first == self.second

    @property
    def same_length(self) -> bool:
        return len(self.first) == len(self.second)

    def report(self) -> str:
        """Retornar texto permite exibi-lo, testá-lo ou salvá-lo depois."""
        title = "Comparação das duas strings"
        separator = "=" * len(title)
        length_message = (
            "As duas strings são de mesmo tamanho."
            if self.same_length
            else "As duas strings são de tamanhos diferentes."
        )
        content_message = (
            "As duas strings possuem o mesmo conteúdo."
            if self.same_content
            else "As duas strings possuem conteúdo diferente."
        )
        return "\n".join([
            title, separator,
            f"String 1: {self.first}",
            f"String 2: {self.second}",
            f"Tamanho String 1: {len(self.first)}",
            f"Tamanho String 2: {len(self.second)}",
            separator, length_message, content_message,
        ])


@dataclass(frozen=True)
class PhoneNumber:
    """Regra do exercício: sete dígitos recebem 3; oito são preservados.

    Não representa as regras atuais de telefonia brasileira.
    """

    original: str

    def __post_init__(self) -> None:
        if len(self.digits) not in (7, 8) or not all(
            "0" <= digit <= "9" for digit in self.digits
        ):
            raise ValueError("Informe sete ou oito dígitos, com ou sem hífen.")

    @property
    def digits(self) -> str:
        # Só removemos o separador permitido; letras não desaparecem silenciosamente.
        return self.original.replace("-", "")

    @property
    def needs_correction(self) -> bool:
        return len(self.digits) == 7

    @property
    def corrected(self) -> str:
        return "3" + self.digits if self.needs_correction else self.digits

    @property
    def formatted(self) -> str:
        number = self.corrected
        return f"{number[:4]}-{number[4:]}"

    def report(self) -> str:
        message = f"Telefone possui {len(self.digits)} dígitos."
        if self.needs_correction:
            message += " Vou acrescentar o dígito três na frente."
        return "\n".join([
            "Valida e corrige número de telefone",
            f"Telefone: {self.original}",
            message,
            f"Telefone corrigido sem formatação: {self.corrected}",
            f"Telefone corrigido com formatação: {self.formatted}",
        ])


def main() -> None:
    print(StringComparison("Brasil Hexa 2006", "Brasil! Hexa 2006!").report())
    print()
    print(PhoneNumber("461-0133").report())


if __name__ == "__main__":
    main()
