import asyncio

async def on_event(partition_context, event):
    print("Received event:", event.body_as_str())
    # Process the event here

async def start_listening():
    print("package is created from github and running .....")
    # Async operations go here, make sure to use 'await' for each async call

def main():
    asyncio.run(start_listening())

if __name__ == "__main__":
    main()

