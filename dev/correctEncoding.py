import os

for i in os.listdir("../templates"):
    with open("../templates/" + i, "r") as f:
        content = f.read()
    with open("../templates/" + i, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Processed {i} to ensure UTF-8 encoding.")
    # break # test 

input("Finish...")