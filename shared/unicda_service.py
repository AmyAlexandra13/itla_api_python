import logging
import requests
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import json


class UNICDAService:
    def __init__(self):
        self.base_url = "https://localhost:7192"
        self.institucion_externa_id = 1
        self.token_secreto = "qB6Ev-zD6Nd8K6f1JOqaKzweqbXexpYPC_2RDttTdDu_v6JsAZmozxFM"
        self.access_token = None
        self.token_expiry = None

    def _generate_external_token(self) -> Optional[str]:
        """
        Genera un token de acceso externo para autenticarse con la API de UNICDA
        """
        try:
            url = f"{self.base_url}/api/Auth/GenerateExternalAPIToken"

            payload = {
                "institucionExternaId": self.institucion_externa_id,
                "token": self.token_secreto
            }

            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }

            # Deshabilitar verificación SSL para localhost (solo para desarrollo)
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                verify=False,
                timeout=30
            )

            if response.status_code == 200:
                response_data = response.json()

                # Asumir que la respuesta contiene el token y posiblemente la expiración
                if isinstance(response_data, dict):
                    token = response_data.get('token') or response_data.get('accessToken')
                    expires_in = response_data.get('expiresIn', 3600)  # Default 1 hora
                elif isinstance(response_data, str):
                    token = response_data
                    expires_in = 3600  # Default 1 hora
                else:
                    token = str(response_data)
                    expires_in = 3600

                if token:
                    self.access_token = token
                    self.token_expiry = datetime.now() + timedelta(seconds=expires_in)
                    logging.info("Token de UNICDA generado exitosamente")
                    return token
                else:
                    logging.error("No se recibió token en la respuesta de UNICDA")
                    return None
            else:
                logging.error(f"Error al generar token de UNICDA: {response.status_code} - {response.text}")
                return None

        except requests.exceptions.SSLError as e:
            logging.error(f"Error SSL al conectar con UNICDA: {str(e)}")
            return None
        except requests.exceptions.ConnectionError as e:
            logging.error(f"Error de conexión con UNICDA: {str(e)}")
            return None
        except requests.exceptions.Timeout as e:
            logging.error(f"Timeout al conectar con UNICDA: {str(e)}")
            return None
        except Exception as e:
            logging.error(f"Error inesperado al generar token de UNICDA: {str(e)}")
            return None

    def _is_token_valid(self) -> bool:
        """
        Verifica si el token actual es válido y no ha expirado
        """
        if not self.access_token or not self.token_expiry:
            return False

        # Renovar el token 5 minutos antes de que expire
        return datetime.now() < (self.token_expiry - timedelta(minutes=5))

    def get_valid_token(self) -> Optional[str]:

        if not self._is_token_valid():
            logging.info("Token de UNICDA expirado o inexistente, generando nuevo token")
            return self._generate_external_token()

        return self.access_token

    def make_authenticated_request(
            self,
            method: str,
            endpoint: str,
            data: Optional[Dict[str, Any]] = None,
            params: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        try:
            token = self.get_valid_token()
            if not token:
                logging.error("No se pudo obtener token válido de UNICDA")
                return None

            url = f"{self.base_url}{endpoint}"

            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }

            response = requests.request(
                method=method.upper(),
                url=url,
                headers=headers,
                json=data if data else None,
                params=params if params else None,
                verify=False,
                timeout=30
            )

            if response.status_code in [200, 201, 204]:
                if response.content:
                    try:
                        return response.json()
                    except json.JSONDecodeError:
                        return {"message": "Success", "content": response.text}
                else:
                    return {"message": "Success"}
            else:
                logging.error(f"Error en petición a UNICDA: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            logging.error(f"Error inesperado en petición a UNICDA: {str(e)}")
            return None

    # Métodos de conveniencia para operaciones comunes
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Realiza una petición GET autenticada"""
        return self.make_authenticated_request("GET", endpoint, params=params)

    def post(self, endpoint: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Realiza una petición POST autenticada"""
        return self.make_authenticated_request("POST", endpoint, data=data)

    def put(self, endpoint: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Realiza una petición PUT autenticada"""
        return self.make_authenticated_request("PUT", endpoint, data=data)

    def delete(self, endpoint: str) -> Optional[Dict[str, Any]]:
        """Realiza una petición DELETE autenticada"""
        return self.make_authenticated_request("DELETE", endpoint)


unicda_service = UNICDAService()