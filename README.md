# Link Tracker — Paso 3 (Estructura del repo)
Desfío 3. El desafío
Cree una API de backend de seguimiento de enlaces que haga lo siguiente:
1.	Cuando un usuario hace clic en un enlace, se debe activar una solicitud HTTPS a un punto final de API Gateway o AppSync.
2.	Detrás del punto final de API Gateway o AppSync debe haber una función Lambda para procesar el evento
3.	La función Lambda debe registrar este evento en una base de datos como AWS DynamoDB
4.	Luego, Lambda debería devolver una respuesta JSON después de guardar el evento en la base de datos.
Requisitos
1.	Toda la infraestructura de AWS debe automatizarse con IAC utilizando Serverless Framework y CloudFormation según sea necesario
2.	Un repositorio público de GitHub debe compartirse con confirmaciones frecuentes
3.	Se debe grabar un video ( www.loom.com ) de usted hablando sobre el código de la aplicación, IAC y cualquier área adicional que desee resaltar en su solución para demostrar habilidades adicionales.
Por favor, dedique a esto únicamente el tiempo que considere razonable
Desarrollo: 
Este repo es el esqueleto del Desafío 3.
Archivos:
- handler.py
- serverless.yml
- requirements.txt
- .gitignore
- README.md

Siguiente:
 .Paso 1. Estrucura del github
<img width="1370" height="785" alt="Captura de pantalla 2025-10-12 220504" src="https://github.com/user-attachments/assets/402821d3-dff2-4806-bf7c-37b4f9c7aa62" />

 _Paso 2. 
 Paso 3: Funcion lambda
 <img width="1428" height="790" alt="Captura de pantalla 2025-10-12 182340funcioneslambdalink-trackerdev-prod" src="https://github.com/user-attachments/assets/1dc806d5-607f-4a3c-b7cf-5e37d728e652" />

- Paso 4: Infra (DynamoDB + Lambda + HTTP API) en `serverless.yml`.
- Paso 5: Implementar `track_click` en `handler.py`.
 Stage Dev

<img width="1211" height="301" alt="Captura de pantalla 2025-10-12 180642stagedevdeploy" src="https://github.com/user-attachments/assets/d4c7c91c-790c-4dd9-88c2-de0409f3c1c2" />
Stage Prod

<img width="1211" height="301" alt="Captura de pantalla 2025-10-12 180642stagedevdeploy" src="https://github.com/user-attachments/assets/4df16f98-78c7-4d9c-bc84-96e025458889" />

Paso 6. Visualización en aws link-trackerclick
