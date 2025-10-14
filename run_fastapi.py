import uvicorn

if __name__ == "__main__":
    uvicorn.run("utils.miniapp_server:app", host="0.0.0.0", port=8080, reload=True)
