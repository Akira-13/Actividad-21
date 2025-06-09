#!/usr/bin/env python3
"""
Punto de entrada que une todos los patrones para generar una configuración
Terraform completamente local en formato JSON.

El archivo resultante puede aplicarse con:

    $ cd terraform
    $ terraform init
    $ terraform apply

No se requieren credenciales de nube, demonio de Docker, ni dependencias externas.
"""

import os
from iac_patterns.builder import InfrastructureBuilder
from iac_patterns.singleton import ConfigSingleton
from iac_patterns.factory import TimestampedNullResourceFactory
def main() -> None:
    # Inicializa una configuración global única para el entorno "local-dev"
    config = ConfigSingleton(env_name="desarrollo-local")
    config.set("proyecto", "patrones_iac_locales")

    # Construye la infraestructura usando el nombre de entorno desde la configuración global
    builder = InfrastructureBuilder(env_name=config.env_name)

    # Construye 15 recursos null ficticios para demostrar escalabilidad (>1000 líneas en total)
    builder.build_null_fleet(count=15)

    
    block = TimestampedNullResourceFactory.create("my_timestamped", "%Y%m%d")
    builder._module.add(block)


    # Agrega un recurso final personalizado con una nota descriptiva
    builder.add_custom_resource(
        name="finalizador",
        triggers={"nota": "Recurso compuesto generado dinámicamente en tiempo de ejecución"}
    )

    # Exporta el resultado a un archivo Terraform JSON en el directorio especificado
    builder.export(path=os.path.join("terraform", "main.tf.json"))
    
    builder = InfrastructureBuilder(env_name=config.env_name)
    builder.build_group("my_group", 3)
    builder._export("terraform/my_group.tf.json")

    builder = InfrastructureBuilder(env_name=config.env_name)
    builder.build_null_fleet(15).export("terraform/main15.tf.json")

    builder = InfrastructureBuilder(env_name=config.env_name)
    builder.build_null_fleet(150).export("terraform/main150.tf.json")
    
# Ejecuta la función principal si el archivo se ejecuta directamente
if __name__ == "__main__":
    main()
