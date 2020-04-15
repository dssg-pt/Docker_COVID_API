# Docker_COVID_API

Tipos de requests possíveis até à data:

## /get_full_dataset

Retorna um json com o dataset inteiro. O Json vem no formato:

dict like {index -> {column -> value}}

## /get_status

Retorna um status de 200 se o servidor estiver online

## /get_last_update

Retorna um json com a última entrada do dataset. O Json vem no formato:

dict like {index -> {column -> value}}

## /get_entry/<string:date>

Deve ser feito no formato dia-mês-ano. Por exemplo /get_entry/01-04-2020

Retorna um json com a entrada da data pedida. O Json vem no formato:

dict like {index -> {column -> value}}

Caso não seja encontrada a data no dataset é retornado um erro.

## /get_entry/<string:date_1>_until_<string:date_2>

Deve ser feito no formato dia-mês-ano. Por exemplo /get_entry/01-04-2020_until_05-04-2020

Retorna um json com as entradas do intervado de dados pedido. O Json vem no formato:

dict like {index -> {column -> value}}

Caso não seja encontrada uma das datas no dataset é retornado um erro.