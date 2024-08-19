import datetime
import random
import time
import requests
import json
import logging
import pytz
from config.config import INTEREST_RATE, MAX_SLEEP_TIME, MIN_SLEEP_TIME, NUMBER_OF_PERIODS, RESERVATION_AMOUNT, TABLE_ID

class APIClient:
    def __init__(self, api_url, token):
        self.api_url = api_url
        self.token = token
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {token}"
        }

    def create_simulation(self, cpf):
        url = f"{self.api_url}/fgts/create-simulation"
        payload = {
            "tableId": TABLE_ID,
            "reservationAmount": RESERVATION_AMOUNT,
            "numberOfPeriods": NUMBER_OF_PERIODS,
            "interestRate": INTEREST_RATE,
            "cpf": cpf
        }
        response = requests.post(url, json=payload, headers=self.headers)
        if response.status_code == 201:
            simulation_id = response.json()['id']
            logging.info(f"Simulação criada com sucesso: {simulation_id} | {cpf}")
            return simulation_id
        elif response.status_code == 429:
            time_to_sleep = random.uniform(MIN_SLEEP_TIME, MAX_SLEEP_TIME)
            logging.warning(f"Too Many Requests as send for Lotus, Sleeping for {time_to_sleep} seconds")
            time.sleep(time_to_sleep)
            return self.create_simulation(cpf)
        else:
            logging.error(f"Erro ao criar simulação para o cpf : {cpf} | {response.text}")
            return None

    def get_simulation_result(self, simulation_id):
        url = f"{self.api_url}/fgts/simulation/{simulation_id}"
        while True:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                simulation_result = response.json()
                if simulation_result['status'] == 'COMPLETED':
                    reservation_amount = simulation_result["simulation"]['totalTransfer']
                    logging.info(f"Simulação concluída com sucesso: {reservation_amount} | {cpf}")
                    result_dict = {
                        "status": simulation_result["status"],
                        "message": "Limite Disponível",
                        "valor_liberado": reservation_amount,
                        "cpf": cpf,
                        "simulation_id": simulation_id,
                        "processed_at": datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%Y-%m-%d %H:%M:%S")
                    }
                    return result_dict
                else:
                    logging.info(f"Simulação ainda em processo... {simulation_id} | {cpf}")
                    time.sleep(16)
            else:
                error_response = response.text
                try:
                    error_dict = json.loads(error_response)
                except json.JSONDecodeError:
                    error_dict = {"error": error_response}
                
                error_dict["valor_liberado"] = 0
                error_dict["cpf"] = cpf
                error_dict["simulation_id"] = simulation_id
                error_dict["processed_at"] = datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%Y-%m-%d %H:%M:%S")
                message = error_dict["message"] 
                error_dict["message"] = message.replace("\n","")
                logging.warning(f"Erro ao obter resultado da simulação: {simulation_id} | CPF: {cpf}")
                return error_dict