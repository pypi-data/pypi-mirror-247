
# mockTestIC
Este script Python utiliza a biblioteca Faker para gerar dados fictícios de acordo com as chaves especificadas em um dicionário de entrada. A função principal é fakeJson, que recebe um dicionário json_data contendo chaves que representam tipos de dados desejados e valores associados a esses tipos.



## Dicionário
``` 
        "primeiroNome": fake.first_name,
        "sobreNome": fake.last_name,
        "nomeCompleto": fake.name,
        "nomeUser": fake.user_name,
        "prefixo": fake.prefix,
        "suffix": fake.suffix,
        "endereco": fake.address,
        "cidade": fake.city,
        "estado": fake.state,
        "pais": fake.country,
        "codigoPostal": fake.zipcode,
        "enderecoRua": fake.street_address,
        "latitude": fake.latitude,
        "longitude": fake.longitude,
        "numeroTelefone": fake.phone_number,
        "email": fake.email,
        "emailSeguro": fake.safe_email,
        "dataNasc": fake.date_of_birth,
        "dataSec": fake.date_this_century,
        "dataDec": fake.date_this_decade,
        "horario": fake.time,
        "dataHora": fake.date_time,
        "horaISO": fake.iso8601,
        "frase": fake.sentence,
        "paragrafo": fake.paragraph,
        "texto": fake.text,
        "empresa": fake.company,
        "cargo": fake.job,
        "segurancaSocial": fake.ssn,
        "numeroInteiro": fake.random_int,
        "elemento": fake.random_element,
        "amostra": fake.random_sample,
        "numeroFlutuante": fake.pyfloat,
        "url": fake.url,
        "ipv4": fake.ipv4,
        "ipv6": fake.ipv6,
        "numeroCartao": fake.credit_card_number,
        "cartaoVencimento":fakecredit_card_expire, 
 ```
# Como usar

Para utilizar a biblioteca mockTestIC, primeiro é necessário instalá-la. Você pode fazer isso executando o seguinte comando no terminal: 

``` 
    pip install mockTestIC
```

Após a instalação, importe a biblioteca no seu código da seguinte maneira:

``` 
    from mockTestIC import fakeJson
```

Agora, abaixo, você encontra um exemplo de como implementar a biblioteca:

```
    from mockTestIC import fakeJson  

dados_json = {
    "primeiro nome": "primeiroNome",
    "sobrenome": "sobreNome",
    "nome completo": "nomeCompleto",
    "nome user": "nomeUser",
    "prefixo": "prefixo",
    "suffix": "suffix",
}

dados_gerados = fakeJson(dados_json)

print(dados_gerados)

```

Lembre-se de que o nome do campo no dicionário dados_json pode ser qualquer um; apenas o valor associado a cada chave deve seguir a formatação especificada.

Abaixo está a lista dos tipos de dados suportados pela biblioteca, que podem ser utilizados como valores no dicionário dados_json

```
    {
    "primeiroNome": "primeiroNome",
    "sobreNome": "sobreNome",
    "nomeCompleto": "nomeCompleto",
    "nomeUser": "nomeUser",
    "prefixo": "prefixo",
    "suffix": "suffix",
    "endereco": "endereco",
    "cidade": "cidade",
    "estado": "estado",
    "pais": "pais",
    "codigoPostal": "codigoPostal",
    "enderecoRua": "enderecoRua",
    "latitude": "latitude",
    "longitude": "longitude",
    "numeroTelefone": "numeroTelefone",
    "email": "email",
    "emailSeguro": "emailSeguro",
    "dataNasc": "dataNasc",
    "dataSec": "dataSec",
    "dataDec": "dataDec",
    "horario": "horario",
    "dataHora": "dataHora",
    "horaISO": "horaISO",
    "frase": "frase",
    "paragrafo": "paragrafo",
    "texto": "texto",
    "empresa": "empresa",
    "cargo": "cargo",
    "segurancaSocial": "segurancaSocial",
    "numeroInteiro": "numeroInteiro",
    "elemento": "elemento",
    "amostra": "amostra",
    "numeroFlutuante": "numeroFlutuante",
    "url": "url",
    "ipv4": "ipv4",
    "ipv6": "ipv6",
    "numeroCartao": "numeroCartao",
    "cartaoVencimento": "cartaoVencimento"
}
```
Utilize esse exemplo e adapte conforme necessário para fornecer uma documentação clara e útil aos usuários da sua biblioteca.





# Contato

Email: Victoraugustodocarmo32@gmail.com