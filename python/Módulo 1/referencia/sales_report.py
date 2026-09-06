"""Relatório de vendas: python sales_report.py --help. Sem envio por padrão."""

import argparse
import os
import re
import smtplib
import unicodedata
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from email.message import EmailMessage
from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd


@dataclass(frozen=True)
class SalesSummary:
    revenue: Decimal
    quantity: int

    def report(self) -> str:
        # Formato fixo do relatório, independente do locale instalado no sistema.
        amount = format(self.revenue, ",.2f").translate(str.maketrans(",.", ".,"))
        return (
            "Bom dia!\n\nSegue o relatório de vendas:\n"
            f"Quantidade de produtos vendidos: {self.quantity}\n"
            f"Faturamento: R$ {amount}\n"
        )


class SalesAnalyzer:
    """Contrato: valores numéricos finitos; quantidade inteira; sem células vazias.

    Valores monetários em texto usam ponto decimal, sem moeda ou milhar.
    Negativos são aceitos para representar estornos. Não arredondamos entradas.
    """

    REQUIRED_COLUMNS = ("VALOR_FINAL", "QUANTIDADE")

    @staticmethod
    def _normalize_header(value: object) -> str:
        text = unicodedata.normalize("NFKD", str(value))
        text = "".join(char for char in text if not unicodedata.combining(char))
        return re.sub(r"[^A-Z0-9]+", "_", text.upper()).strip("_")

    @staticmethod
    def _parse_number(value: object, column: str, position: int) -> Decimal:
        try:
            number = Decimal(str(value))
        except (InvalidOperation, ValueError):
            raise ValueError(f"{column}, registro {position}: número inválido.") from None
        if not number.is_finite():
            raise ValueError(f"{column}, registro {position}: valor ausente ou não finito.")
        return number

    def summarize(self, data: pd.DataFrame) -> SalesSummary:
        table = data.copy()
        table.columns = [self._normalize_header(name) for name in table.columns]
        if table.columns.duplicated().any():
            raise ValueError("Há nomes de colunas duplicados após a normalização.")
        missing = set(self.REQUIRED_COLUMNS) - set(table.columns)
        if missing:
            raise ValueError(f"Colunas obrigatórias ausentes: {', '.join(sorted(missing))}.")
        if table.empty:
            raise ValueError("A base está vazia; nenhum relatório será gerado.")

        revenue = Decimal("0")
        quantity = 0
        for position, (amount, count) in enumerate(
            table.loc[:, list(self.REQUIRED_COLUMNS)].itertuples(index=False, name=None),
            start=1,
        ):
            amount = self._parse_number(amount, "VALOR_FINAL", position)
            count = self._parse_number(count, "QUANTIDADE", position)
            if amount != amount.quantize(Decimal("0.01")):
                raise ValueError(f"VALOR_FINAL, registro {position}: há frações de centavo.")
            if count != count.to_integral_value():
                raise ValueError(f"QUANTIDADE, registro {position}: deve ser inteira.")
            revenue += amount
            quantity += int(count)
        return SalesSummary(revenue, quantity)


class ExcelSource:
    def read(self, path: Path) -> pd.DataFrame:
        if path.suffix.lower() != ".xlsx" or not path.is_file():
            raise ValueError(f"Informe um arquivo .xlsx existente: {path}")
        return pd.read_excel(path, engine="openpyxl")


class DriveSource:
    def download(self, url: str, destination: Path, filename: str) -> Path:
        import gdown

        paths = gdown.download_folder(url=url, output=str(destination), quiet=True)
        candidates = [Path(path) for path in (paths or []) if Path(path).name == filename]
        if len(candidates) != 1:
            raise ValueError(
                f"Esperado exatamente um arquivo chamado {filename!r}; "
                f"encontrados {len(candidates)}."
            )
        return candidates[0].resolve()


@dataclass(frozen=True)
class GmailSender:
    username: str
    password: str = field(repr=False)

    def send(self, summary: SalesSummary, recipient: str) -> None:
        message = EmailMessage()
        message["Subject"] = "Automação Python - Relatório de Faturamento"
        message["From"] = self.username
        message["To"] = recipient
        message.set_content(summary.report())
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as smtp:
            smtp.login(self.username, self.password)
            smtp.send_message(message)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--file", type=Path, help="Base Excel local")
    source.add_argument("--drive-url", help="Pasta pública do Google Drive")
    parser.add_argument("--filename", help="Nome exato do Excel dentro da pasta do Drive")
    parser.add_argument("--send-to", help="Envia via Gmail; omitido, apenas exibe o relatório")
    args = parser.parse_args()
    if args.drive_url and not args.filename:
        parser.error("--drive-url exige --filename")

    sender = None
    if args.send_to:
        username = os.environ.get("GMAIL_USER")
        password = os.environ.get("GMAIL_APP_PASSWORD")
        if not username or not password:
            parser.error("Defina GMAIL_USER e GMAIL_APP_PASSWORD antes de enviar.")
        sender = GmailSender(username, password)

    # Cada execução tem sua pasta: arquivos antigos não entram na seleção.
    with TemporaryDirectory(prefix="sales-report-") as directory:
        path = args.file or DriveSource().download(
            args.drive_url, Path(directory), args.filename
        )
        summary = SalesAnalyzer().summarize(ExcelSource().read(path))
    print(summary.report())
    if sender is not None:
        sender.send(summary, args.send_to)
        print("Mensagem aceita pelo servidor SMTP.")


if __name__ == "__main__":
    main()
