import pandas as pd
from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine, text

from langflow.custom import Component
from langflow.schema import Data
from langflow.io import Output


class EFLegacyDB(Component):
    display_name = "Redshift via SSH"
    description = "Query Redshift over SSH and return DataFrame"
    documentation: str = "---"
    icon = "database"
    name = "EFLegacyDB"

    outputs = [
        Output(display_name="Output", name="output", method="build_output"),
    ]

    def build_output(self) -> Data:
        ssh_host = "ec2-54-191-186-159.us-west-2.compute.amazonaws.com"
        ssh_port = 22
        ssh_user = "ec2-user"
        ssh_key_path = "/app/ef_redshift_id_rsa_pub"

        redshift_user = "readonlyfull"
        redshift_password = "FBXGzy6F2Ug3S3du"
        redshift_host = "testing-upsert.cxsxrw6itdqy.us-west-2.redshift.amazonaws.com"
        redshift_port = 5439
        redshift_db = "upsert"

        try:
            with SSHTunnelForwarder(
                (ssh_host, ssh_port),
                ssh_username=ssh_user,
                ssh_pkey=ssh_key_path,
                remote_bind_address=(redshift_host, redshift_port),
                local_bind_address=("127.0.0.1", 5432)
            ) as tunnel:
                # SQLAlchemy connection string pointing to the forwarded port
                sqlalchemy_url = f"postgresql+psycopg2://{redshift_user}:{redshift_password}@127.0.0.1:{tunnel.local_bind_port}/{redshift_db}"
                engine = create_engine(
                    sqlalchemy_url,
                    connect_args={"options": "-c search_path=public"}
                )

                query = "SELECT current_date;"  # Replace with any query you need
                df = pd.read_sql_query(text(query), engine)

                return Data(value=df)

        except Exception as e:
            return Data(value=pd.DataFrame({"error": [str(e)]}))