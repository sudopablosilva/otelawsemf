# syntax=docker/dockerfile:1

# Stage 1: Dependencies
FROM eclipse-temurin:20-jdk as deps
WORKDIR /build
RUN apt-get update && apt-get install -y maven
COPY pom.xml ./
RUN mvn dependency:go-offline -DskipTests

# Stage 2: Build
FROM deps as build
COPY src src
RUN mvn clean package -DskipTests && cp target/demo-0.0.1-SNAPSHOT.jar app.jar

   
# Stage 3: Final Image
FROM eclipse-temurin:20-jdk AS final
WORKDIR /app

# Copy the built application JAR from the build stage
COPY --from=build /build/app.jar app.jar

# Download OpenTelemetry Java agent
RUN curl -sSL -o opentelemetry-javaagent.jar \
    # https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases/download/v2.9.0/opentelemetry-javaagent.jar
    https://github.com/aws-observability/aws-otel-java-instrumentation/releases/download/v1.32.5/aws-opentelemetry-agent.jar

# Set environment variables for OpenTelemetry configuration
ENV JAVA_TOOL_OPTIONS="-javaagent:/app/opentelemetry-javaagent.jar"
# Disable traces, logs, and enable only metrics
# ENV OTEL_METRICS_EXPORTER="otlp" \
#     OTEL_TRACES_EXPORTER="none" \
#     OTEL_LOGS_EXPORTER="none" \
#     OTEL_EXPORTER_OTLP_ENDPOINT="http://otel-collector:4317"


RUN apt-get update && apt-get install -y unzip
# Verify app.jar exists and has the expected manifest attribute
RUN test -f app.jar && \
    echo "app.jar exists." && \
    if unzip -p app.jar META-INF/MANIFEST.MF | grep -q "Main-Class"; then \
        echo "Manifest contains Main-Class attribute."; \
    else \
        echo "ERROR: Main-Class attribute missing in manifest!" >&2; \
        exit 1; \
    fi

# Verify that the JAR contains dependencies in BOOT-INF/lib/
RUN if jar tf app.jar | grep -q "BOOT-INF/lib/"; then \
      echo "Dependencies verified in BOOT-INF/lib/"; \
    else \
      echo "ERROR: Dependencies missing in BOOT-INF/lib/" >&2; \
      exit 1; \
    fi

# Run the application
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
