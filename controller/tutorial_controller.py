from datetime import date as dt

def get_table_backup_codes(name: str) -> list:
    comands = []
    comands.append("cd ..")
    comands.append("cd ..")
    comands.append("cd ./UAPA/vm/ ")
    comands.append('ssh -i "UAPA-prod-vm-1.pem" ec2-user@ec2-3-13-103-119.us-east-2.compute.amazonaws.com')
    comands.append("ls uapapp/backups")

    comands.append("docker exec -it uapapp-uapapp-database-1 bash")
    comands.append("ls backups")

    date = dt.today()
    date_str = f'{date.year}_{date.month}_{date.day}'

    file = f'{name}_backup_{date_str}.sql'

    comands.append(f"mariadb-dump --user=uapapp-admin --password --single-transaction mainDB {name} > /backups/{file}")
    comands.append("F535!vcH@2MA%^8*682s*x6UA@@SE8&gcozAn$&E")
    comands.append('exit')

    comands.append(f'docker cp uapapp-uapapp-database-1:"/backups/{file}" "uapapp/backups/"')
    comands.append('ls uapapp/backups')
    comands.append('exit')

    comands.append(f'scp -i UAPA-prod-vm-1.pem ec2-user@ec2-3-13-103-119.us-east-2.compute.amazonaws.com:uapapp/backups/{file} /UAPA/UPDATES/data/backups')
    return comands

def get_upload_folder_codes(name: str) -> list:
    comands = []
    comands.append("cd ..")
    comands.append("cd ..")
    comands.append("cd ./UAPA/vm/ ")
    comands.append(f'scp -r -i "UAPA-prod-vm-1.pem" .\{name} ec2-user@ec2-3-13-103-119.us-east-2.compute.amazonaws.com:~/uapapp/updates/{name}')
    comands.append('ssh -i "UAPA-prod-vm-1.pem" ec2-user@ec2-3-13-103-119.us-east-2.compute.amazonaws.com')
    comands.append(f'ls uapapp/updates/{name}')
    comands.append(f'docker cp "./uapapp/updates/{name}" uapapp-uapapp-database-1:"/updates/{name}"')
    comands.append("docker exec -it uapapp-uapapp-database-1 bash")
    comands.append(f'cd updates/{name}')
    comands.append('ls')
    comands.append('mariadb --user="uapapp-admin" --database="mainDB" -f -p < ')
    comands.append("F535!vcH@2MA%^8*682s*x6UA@@SE8&gcozAn$&E")
    return comands

