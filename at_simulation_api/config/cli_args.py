import argparse
import os


def parse_db_args(parser: argparse.ArgumentParser):
    group = parser.add_argument_group("Database Configuration")
    group.add_argument("--db_host", type=str, help="Database host.")
    group.add_argument("--db_port", type=int, help="Database port.")
    group.add_argument("--db_name", type=str, help="Database name.")
    group.add_argument("--db_user", type=str, help="Database user.")
    group.add_argument("--db_pass", type=str, help="Database password.")


def parse_minio_args(parser: argparse.ArgumentParser):
    group = parser.add_argument_group("Minio configuration")
    group.add_argument("--minio_host", type=str, help="Minio host.")
    group.add_argument("--minio_access_key", type=str, help="Minio access key.")
    group.add_argument("--minio_secret_key", type=str, help="Minio secret key.")
    group.add_argument("--minio_secure", type=bool, help="Use secure connection.")
    group.add_argument("--minio_bucket_name", type=str, help="Minio bucket name.")
    group.add_argument("--minio_api_port", type=int, help="Minio API port.")
    group.add_argument("--minio_console_port", type=int, help="Minio console port.")


def parse_rabbitmq_args(parser: argparse.ArgumentParser):
    group = parser.add_argument_group("RabbitMQ configuration")
    group.add_argument("--rabbitmq_host", type=str, help="RabbitMQ host.")
    group.add_argument("--rabbitmq_port", type=int, help="RabbitMQ port.")
    group.add_argument("--rabbitmq_login", type=str, help="RabbitMQ login.")
    group.add_argument("--rabbitmq_password", type=str, help="RabbitMQ password.")
    group.add_argument("--rabbitmq_vhost", type=str, help="RabbitMQ virtualhost.")
    group.add_argument("--rabbitmq_ssl", type=bool, help="Use SSL for RabbitMQ.")


def parse_server_args(parser: argparse.ArgumentParser):
    group = parser.add_argument_group("Server configuration")
    group.add_argument("--server_port", type=int, help="Server port.")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Main application configuration.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parse_db_args(parser)
    parse_minio_args(parser)
    parse_rabbitmq_args(parser)
    parse_server_args(parser)
    args = parser.parse_args()

    for key, value in vars(args).items():
        if value is not None:
            os.environ[key.upper()] = str(value)
