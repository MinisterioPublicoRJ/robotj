# robotj
Robo de Extração de Processos do Tribunal de Justiça do Rio de Janeiro


## Configurações e variáveis de ambiente

```
export DB_HOST="(Host do Banco de Dados)"
export DB_USER="(Usuário do Banco de Dados)"
export DB_PASSWORD="(Senha do Usuário do Banco de Dados)"
export DB_SID="(Instância do Banco de Dados)"
export DB_PORT='(Porta do Banco de Dados)'

export NEW_RELIC_PROXY_SCHEME="http"
export NEW_RELIC_PROXY_HOST="(Endereço do Proxy NEw Relic, caso necessário)"
export NEW_RELIC_PROXY_PORT="(Porta do Proxy NEw Relic, caso necessário)"
export NEW_RELIC_PROXY_USER="(Usuário do Proxy, caso necessário)"
export NEW_RELIC_PROXY_PASS="(Senha do Usuário no Proxy)"
export NEW_RELIC_LICENSE_KEY=(Chave de Licença New Relic)
export NEW_RELIC_ENVIRONMENT=(Ambiente New Relic: development|em branco)
export NEW_RELIC_CONFIG_FILE=newrelic.ini 
export NEW_RELIC_LOG=newrelic.log

export QUEUE="(Nome da Fila REDIS para submissão de classificação de Inteiro Teores)"
export BROKER="redis://:[senha]@[host do broker REDIS]:[porta]"

```