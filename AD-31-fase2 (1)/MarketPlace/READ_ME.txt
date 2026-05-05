================================================================================
MarketCenter – Fase 2
================================================================================

GRUPO XX
- Rodrigo Malato (Número 64129)
- Gonçalo Reis (Número 64172)

================================================================================
Descrição
================================================================================
Este projeto constitui a entrega da segunda fase do projeto MarketCenter.

O sistema evoluiu em relação à Fase 1, cumprindo todos os 
requisitos exigidos:
- Arquitetura RPC: Implementação de um `stub` no cliente e um `skeleton` no 
  servidor para abstrair a comunicação em rede.
- Protocolo Estruturado: O envio de comandos em texto livre foi abandonado. 
  A comunicação utiliza listas Python serializadas via `pickle`.
-Implementação da função `_receive_all` e envio 
  de um prefixo de 4 bytes (`struct`) para garantir a receção integral das 
  mensagens, resolvendo o problema natural de fragmentação das streams TCP.
- Multiplexação de I/O: O servidor suporta múltiplos clientes em simultâneo 
  utilizando a chamada de sistema `select()`. As ligações mantêm-se abertas e
  não foi utilizado `threading` ou `multiprocessing`.
- Tratamento Estruturado de Erros: A lógica de negócio lança exceções limpas 
  que o `skeleton` traduz para códigos de erro da série 3xxxx. O cliente traduz
  estes códigos para outputs amigáveis.
- Segurança e Perfis: O servidor valida as permissões de acesso (Anónimo, 
  Registado, Funcionário, Admin) centralmente no `skeleton`.

Requisitos:
Python 3.x (recomendado 3.8 ou superior)

================================================================================
COMO CORRER O PROJETO NO VISUAL CODE / TERMINAL
================================================================================

Como Iniciar o Servidor:
    Na pasta raiz do projeto (MarketPlace):
    python3 -m servidor.main_loja <porto>

Iniciar o Cliente:
    Abrir outro terminal, ainda na pasta raiz:
    python3 -m cliente.main <porto>

Exemplos de Interação:
    Ao iniciar o cliente, será pedida a autenticação base:
    CLIENTE> Introduza o seu Perfil (0:Anónimo, 1:Registado, 2:Funcionário, 3:Admin): 3
    CLIENTE> Introduza o seu ID de Utilizador: 1

    Como criar categoria (apenas permitido a Admin):
    CRIA_CATEGORIA "Eletronica Premium"
    (Se o nome tiver espaços, deve ser colocado entre aspas ou pelicas).

Como encerrar o Servidor:
    No terminal onde o servidor está a correr, escreva diretamente:
    EXIT ou QUIT
    Isto fechará todas as ligações de clientes ativos de forma controlada.

================================================================================
Notas Finais: 
================================================================================
Execute sempre os comandos a partir da pasta raiz do projeto (ex: cd MarketPlace).
Use "python3 -m ..." para evitar problemas de imports.
