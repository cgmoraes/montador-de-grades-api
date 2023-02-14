# API de Disciplinas
Este repositório contém uma API que oferece dois endpoints para lidar com disciplinas disponíveis e suas informações. A API é baseada em Python e usa o framework Flask para gerenciar as rotas e as requisições.

## Endpoints Disponíveis
A seguir, apresentamos uma lista dos endpoints disponíveis nessa API:

### 1. Listar todas as disciplinas disponíveis
Endpoint: GET /disciplinas

Esse endpoint permite que o usuário liste todas as disciplinas disponíveis. A resposta retorna um array de objetos com as informações das disciplinas. 
Cada objeto contém os seguintes campos:

* ID: um identificador único da disciplina;
* NOME: o nome da disciplina;
* TURMA: a turma da disciplina.
* PROFESSORES: os professores da disciplina
* DIA: os dias que a disciplina é ofertada
* HORARIO: os horários que a disciplina é ofertada

Exemplo de resposta:

```sh
GET /disciplinas
[
  {
      "ID": 0,
      "NOME": "Algoritmos e Estruturas de Dados",
      "TURMA": "A",
      "PROFESSORES": "Olavo",
      "DIA": [
        "Segunda",
        "Quarta"
      ],
      "HORARIO": [
        "13h30-15h30",
        "13h30-15h30"
      ]
    },
    {
      "ID": 1,
      "NOME": "Cálculo em uma Variável",
      "TURMA": "B",
      "PROFESSORES": "Claudio",
      "DIA": [
        "Segunda",
        "Quarta"
      ],
      "HORARIO": [
        "19h00-21h00",
        "19h00-21h00"
      ]
    }
  ]
  ```
  
### 2. Retornar disciplinas disponíveis
Endpoint: POST /disciplinas

Esse endpoint retorna as disciplinas que ainda estão disponíveis levando em conta horário, dia e disciplinas de mesma equivalência. 
O usuário deve enviar um json de chave "items" no qual apresenta uma lista com os ids das disciplinas inscritas.

Exemplo de requisição:

```sh
POST /disciplinas
{
  "items": [
    2,
    54,
    27
  ]
}
```

# Rodando a API
A API trabalha em conjunto com o projeto [montador-de-grade](https://github.com/vpedrota/montador-de-grades), executa utilizando os serviços da [GCP](https://www.googleadservices.com/pagead/aclk?sa=L&ai=DChcSEwiSvZzZhZb9AhWIQUgAHTcgBeUYABABGgJjZQ&ohost=www.google.com&cid=CAESbOD2udtgUB7t_UtjTlNaddbAL5IbF1WWHLsPG0Zuc3fnq0Oje6TUJGdeyp4Q3tHFRwApPeQ2Fajm5FZ__HFIwaO2vJG-V2cAgCe8liM0dgiBwS2uVZS_WzYIw-wlRiWErAIjsn4hFrQ3FY7QGA&sig=AOD64_3yvHegme8lXDnEgTHI7YAmXgA0dA&q&adurl&ved=2ahUKEwi67pTZhZb9AhUGqpUCHav3ATEQ0Qx6BAgJEAE) e está disponível no seguinte endereço: https://montadordegrades.online/.
