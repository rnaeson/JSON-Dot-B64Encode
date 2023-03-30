import os
import sys
import json
import base64

COMPLETE = '✅'
ERR = '❌'

# def Write2File(fileName, listFile):
#     """This function write the list files out as JSON files to the file system."""
#     try:
#         logging.debug("Writeing data records to disk...")
#         File = open(fileName, "w")
#         File.write(listFile)    
#         File.close()
#     except Exception as e:
#         logging.error(f"An error has been encountered attempting to write the output file to the specified location: {e}")
#         raise(e)


# def lambda_context(custom=None,
#                    env=None,
#                    client=None):
#     client_context = dict(
#         custom=custom,
#         env=env,
#         client=client)
#     json_context = json.dumps(client_context).encode('utf-8')
#     return base64.b64encode(json_context).decode('utf-8')

# context = {
#     "custom": {"foo": "bar"},
#     "env": {"test": "test"},
#     "client": {}
# }

# client.invoke(FunctionName="<YOUR_LAMBDA_FUNCTIONS>",
#                          ClientContext=lambda_context(**context),
#                          Payload=YOUR_PAYLOAD)

def validateJSON(jsonfile):
    try:
        json.load(jsonfile)
    except ValueError as err:
        return False
    return True


if __name__ == "__main__":
    try:
        # Take all provided arguments ommiting 0 (0 is just the name of this script)
        arguments = sys.argv[1:]

        # Only 1 arugument (file) should have been given
        if isinstance(arguments, list) and len(arguments) == 1:
            arg = arguments[0]
            print(f"\nProcessing File: {arg}...")
            
            # Check if the file Exists
            if os.path.exists(arg):
                print(f"File path {arg} path validation... {COMPLETE}")
                
                # Open the file
                fileObj = open(arg)

                # Validate the file is proper json and reset the io object read marker
                jsonvalidated = validateJSON(fileObj)
                fileObj.seek(0)
                
                if jsonvalidated:
                    print(f"JSON validation... {COMPLETE}")
                    print(f"Base64 Encoding Contents Of: {arg}...\n")

                    # Open the IO object (file contents) and read into a file
                    jsonContent = json.load(fileObj)
                    # print(json.dumps(jsonContent, indent=4))
                    
                    # Base 64 Encode the file contents
                    jsonB64 = base64.b64encode(json.dumps(jsonContent).encode('utf-8'))
                    # Print the Base64 Encoded Value
                    print(f"{jsonB64.decode()}\n")
                # If the JSON wasn't valid then send error
                else:
                    print(f"\nERROR: File {arg} contains invalid JSON. Please check the file and try again!... {ERR}\n")
                    fileObj.close()
                    sys.exit(1)
            # If the input file location doesn't exist
            else:
                # If file doesn't exist, error
                print(f"\nERROR: Specified File {arg} location not found!... {ERR}\n")
                fileObj.close()
                sys.exit(1)
        # This is triggered if more then 1 argument was given
        else:
            print(f"WARNING: Only 1 input was expected but recieved {len(arguments)} {ERR}")
            print(arguments)
        # Close the file if it wasn't previously closed
        fileObj.close()
    except KeyboardInterrupt:
        print("Uh Uh Uh... You didn't say the magic word...")
        fileObj.close()
