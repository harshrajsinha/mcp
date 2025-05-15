for /f "delims== tokens=1,2" %%G in (param.txt) do set %%G=%%H

start "SSMP Server" cmd /k "cd /d  %SSMP_ENV_PATH% & activate & cd /d %SSMP_PATH% & uvicorn server:app --port 9000 --reload"
start "LLM Service" cmd /k "cd /d %LLMSERVICE_ENV_PATH% & activate & cd /d %LLMSERVICE_PATH% & uvicorn main:app --port 8051 --reload"
start "MCP Server" cmd /k "cd /d  %MCPSERVER_ENV_PATH% & activate & cd /d %MCPSERVER_PATH% & python server.py"
start "MCP Client" cmd /k " cd /d %MCPCLIENT_ENV_PATH% & activate & cd /d %MCPCLIENT_PATH% & python client.py"
