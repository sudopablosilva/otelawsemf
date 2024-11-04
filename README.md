# Integração Opentelemetry om AWS EMF

Este projeto contempla o uso de docker-compose para provisionar o opentelemetry collector, uma aplicação python, uma aplicação JAVA 20 springboot, e duas aplicações que enviam requisições a cada 5 segundos.

## Fluxo de dados
### JAVA
request-sender -> java-app -> otel-collector -> AWS CloudWatch

### Python
metric-sender -> otel-collector -> AWS CloudWatch

# Como executar/testar
1. git clone https://github.com/sudopablosilva/otelawsemf.git
2. Colar as credenciais AWS no terminal (é necessário ter permissões CloudWatch)
3. docker compose up --build
4. Abrir o serviço CloudWatch no Console AWS e verificar o loggroup TestLogGroupAWSCollectorLGOfficial (Definido em: https://github.com/sudopablosilva/otelawsemf/blob/main/otel-config.yaml#L16)

## Recriar os containers
5. docker compose down --remove-orphans --volumes

# Referências
- https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Embedded_Metric_Format_Specification.html#CloudWatch_Embedded_Metric_Format_Specification_structure
- https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_MetricDatum.html
