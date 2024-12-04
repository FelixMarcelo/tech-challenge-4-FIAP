# *API para Previsão de Preços de Ativos da Apple com LSTM*

API desenvolvida para prever o preço de fechamento diário de ações financeiras, utilizando técnicas avançadas de aprendizado profundo (Deep Learning). Utilizando Redes Neurais Recorrentes (RNN) com Long Short-Term Memory (LSTM), que são altamente eficazes na análise de séries temporais, como os preços de ações.  

---

## *Objetivo*  
O principal objetivo deste projeto é fornecer uma API para:  
1. Prever o *preço de fechamento do ativo AAPL (Apple)* no próximo dia.  
2. Permitir ao usuário fornecer *dados históricos (preço),* como entrada para a previsão.  
3. Garantir a confiabilidade do modelo por meio de técnicas modernas de monitoramento e validação.  

Além disso, o projeto está preparado para monitoramento e escalabilidade em produção.

---

## 🚀 *Como Executar a API*  

### *1. Configuração Inicial*  
Certifique-se de que você possui Python 3.10.12 ou superior instalado, Docker e docker-compose configurados.  

### *2. Clonar o Repositório e Instalar Dependências*  
```bash
git clone <URL_DO_REPOSITORIO>
```

### *3. Executar a API*

A API foi implementada utilizando o framework FastAPI. Para iniciá-la, use os seguintes comandos na raiz do projeto:
```bash
docker-compose build
docker-compose up -d
```
### *4. Testar a API*

Com a API em execução, acesse a documentação interativa em:
http://localhost:8000/docs

Você pode testar os endpoints diretamente na interface da documentação.

### *5. Monitoração do Modelo*
A Monitoração do modelo será feita através do Prometheus e Grafana.

Prometheus: http://localhost:9090/
Grafana: http://localhost:3000/

#### *5.1 Configuração Grafana

Login: admin
Senha: admin

Para configurar o Prometheus como fonte de dados, siga estes passos: Connections > Data Source > Add new data source > Prometheus

Em seguida, defina a Prometheus server URL: http://host.docker.internal:9090

Agora basta salvar e importar os gráficos com o arquivo "monitoramento_grafana.json", presente no diretório "model", na raiz do seu projeto. 

Caso não saiba como importar gráficos no Grafana, siga estes passos:
Dashboards > New > Import > Upload dashboard JSON file.

Esta configuração só precisará ser feita na primeira vez que utilizar a imagem docker deste projeto.

#### *5.2 Arquitetura

Foi configurado um Scheduler que atualiza as métricas (MAE e RMSE) do modelo com base na previsão dos últimos 30 dias.

Essas métricas são expostas em http://localhost:8000/metrics e são coletadas e armazenadas pelo Prometheus a cada 15 segundos. 

A partir deste processo, o Grafana consegue consumir estes dados e criar gráficos que são atualizados em tempo real. 

---

## 📍  *Valores de Input*


A API aceita dados no formato JSON.

### *1. Dados Históricos*

Um array contendo as informações:

> priceList: Preço de fechamento do ativo na data especificada.


Exemplo de Input:

```bash
{
    "priceList": [150.0, 155.0, 160.0, 158.0, 159.0, 165.0, 170.0, 175.0, 180.0, 185.0,
            190.0, 195.0, 200.0, 205.0, 210.0, 215.0, 220.0, 225.0, 230.0, 235.0,
            240.0, 245.0, 250.0, 255.0, 260.0, 265.0, 270.0, 275.0, 280.0, 285.0,
            290.0, 295.0, 300.0, 305.0, 310.0, 315.0, 320.0, 325.0, 330.0, 335.0,
            340.0, 345.0, 350.0, 355.0, 360.0, 365.0, 370.0, 375.0, 380.0, 385.0,
            390.0, 395.0, 400.0, 405.0, 410.0, 415.0, 420.0, 425.0, 430.0, 435.0,
            440.0, 445.0, 450.0, 455.0, 460.0, 465.0, 470.0, 475.0]
}
```
### *2. Saída Esperada*

A API retorna o preço previsto para o próximo dia:

```bash
{
  "predicted_price": 424.77
}
```

---
## 📝 *Autores*
- Marcelo Felix
- Denise Oliveira