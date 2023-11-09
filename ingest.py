import tempfile
import urllib.request
from langchain.vectorstores import vectara
from langchain.embeddings import FakeEmbeddings
import apis
import os

os.environ["VECTARA_CUSTOMER_ID"] = apis.VECTARA_CUSTOMER_ID
os.environ["VECTARA_CORPUS_ID"]=apis.VECTARA_CORPUS_ID
os.environ["VECTARA_API_KEY"]= apis.VECTARA_API_KEY



urls = [
    [
        "https://vectara.s3.us-east-2.amazonaws.com/loan.txt?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEJX%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCmFwLXNvdXRoLTEiRjBEAiAuMFDCpjSpPBzsbWJ9wsUplOF6GRtPvplvwpL7WPyeCQIgcZNOFtdDPrxSZrB3c34ygZZlY7v92oZkfKK5rAf2sKAq7QIIzv%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw5MzU2MzUzMTEzNDIiDKEKasgX9ZB781odHSrBAsJQ333n9NlClBS6f8VvKcAs7N8xh6ZiBywTKc0yyW9NDlGjOHEY7xP%2BN0%2F9Sq2QZ%2BZXf0qgOf8bCc5tMGHZVgiRAm8Hc76P2OAg7IO6uQuHEjZlOPfiHppv5Dev2%2B%2FZFHqBY3xC5lDg%2B9XmIjfxUNOGicvVbugd%2BpAEAsMO4mtZHDKSE8GQ1GRO54Bpe0tYKlf2T8ZYNxCX20EncubXnbrc8sWcFfjyT9jF%2FvprWPux5QkcuPpPelQOSpmjrz%2B4CEyYN%2BRDIYivCd5hPBrY3XYmHAQr35F7i2bhtGqEqhVeoCEenH8bAppkCWaMx2QYm27U4eyFzXfrO4sSDZFy7CHcj5gdot%2Bbd2YFhdG1L3N9wIlh3Z9WgmyiM9%2FnxkFTvi1MUhZfBPCZfovU8NVzmN5n7pog1qb14T448lYlCNkiQDC3xLGqBjq0AgBXAA3hsIk14FH72tE%2BCOg5u0joaizyXEQx%2Fm7nnTqZgzLAtDthcA9wII%2FZITLh%2Bn%2BAn1uPYsaFgyTfOeNuIAsE2hqz%2FgO%2BlGw49eFP9W2HLotLddmkSin0%2BSkQ3HlGhdigdbR8C1lgQZKjMmpLwmMNGS8yQYlFhtcaUP2TLB9YWBMhHODlbSpelNcjy1u2v1UJCapftvYKO9V1ztYh8%2BE%2BflRzwD4k0qTxb%2F8mc8DTnbXlQQavNg1tDaun7CGxlyCFbmTsqM9C5GavOa3Gf7AnEI2xPNJQkM%2Bf4%2FmFqlU977deD5sFHsA7sMnhzzNDa5qwoOYQ2cF8Mc%2Fd1JBqkgpgCgn2CmPa1JWArNsqFx2LfXqfXPlVeBIbnWPLGcZDz6TckA%2BH1VFg7ZZ8QYns%2FK8N5tLn&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20231109T054138Z&X-Amz-SignedHeaders=host&X-Amz-Expires=299&X-Amz-Credential=ASIA5TWBV3LXLFKTZN5C%2F20231109%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Signature=9bcae8366867718b4a18bd4ffd8a80dc90835838e028b09474215c8f35b9b638",
        "Loans",
        "SIB",
    ],
    [
        "https://vectara.s3.us-east-2.amazonaws.com/service_charges.txt?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEJX%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCmFwLXNvdXRoLTEiRjBEAiAuMFDCpjSpPBzsbWJ9wsUplOF6GRtPvplvwpL7WPyeCQIgcZNOFtdDPrxSZrB3c34ygZZlY7v92oZkfKK5rAf2sKAq7QIIzv%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw5MzU2MzUzMTEzNDIiDKEKasgX9ZB781odHSrBAsJQ333n9NlClBS6f8VvKcAs7N8xh6ZiBywTKc0yyW9NDlGjOHEY7xP%2BN0%2F9Sq2QZ%2BZXf0qgOf8bCc5tMGHZVgiRAm8Hc76P2OAg7IO6uQuHEjZlOPfiHppv5Dev2%2B%2FZFHqBY3xC5lDg%2B9XmIjfxUNOGicvVbugd%2BpAEAsMO4mtZHDKSE8GQ1GRO54Bpe0tYKlf2T8ZYNxCX20EncubXnbrc8sWcFfjyT9jF%2FvprWPux5QkcuPpPelQOSpmjrz%2B4CEyYN%2BRDIYivCd5hPBrY3XYmHAQr35F7i2bhtGqEqhVeoCEenH8bAppkCWaMx2QYm27U4eyFzXfrO4sSDZFy7CHcj5gdot%2Bbd2YFhdG1L3N9wIlh3Z9WgmyiM9%2FnxkFTvi1MUhZfBPCZfovU8NVzmN5n7pog1qb14T448lYlCNkiQDC3xLGqBjq0AgBXAA3hsIk14FH72tE%2BCOg5u0joaizyXEQx%2Fm7nnTqZgzLAtDthcA9wII%2FZITLh%2Bn%2BAn1uPYsaFgyTfOeNuIAsE2hqz%2FgO%2BlGw49eFP9W2HLotLddmkSin0%2BSkQ3HlGhdigdbR8C1lgQZKjMmpLwmMNGS8yQYlFhtcaUP2TLB9YWBMhHODlbSpelNcjy1u2v1UJCapftvYKO9V1ztYh8%2BE%2BflRzwD4k0qTxb%2F8mc8DTnbXlQQavNg1tDaun7CGxlyCFbmTsqM9C5GavOa3Gf7AnEI2xPNJQkM%2Bf4%2FmFqlU977deD5sFHsA7sMnhzzNDa5qwoOYQ2cF8Mc%2Fd1JBqkgpgCgn2CmPa1JWArNsqFx2LfXqfXPlVeBIbnWPLGcZDz6TckA%2BH1VFg7ZZ8QYns%2FK8N5tLn&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20231109T053825Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIA5TWBV3LXLFKTZN5C%2F20231109%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Signature=34451dbe612f4a77de4375f81162f5d7785246675208e325000df53621895183",
        "Interest Rates",
        "SIB",
    ],
]
files_list = []
for url, _, _ in urls:
    name = tempfile.NamedTemporaryFile().name
    urllib.request.urlretrieve(url, name)
    files_list.append(name)

docsearch: Vectara = Vectara.from_files(
    files=files_list,
    embedding=FakeEmbeddings(size=768),
    metadatas=[
        {"url": url, "context": context, "bank": bank} for url, context, bank in urls
    ],
)