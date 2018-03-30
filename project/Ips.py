

def get_hostname(name):
    if name == "dns":
        return "8.8.8.8"
    elif name == "router":
        return "192.168.1.254"
    elif name == "web":
        return "github.com"
    else:
        return "8.8.8.8"


def generate_ips(text):
    parts = text.split(".")

    # TODO fix this
    for i1 in generate_ips_part(parts[0]):
        for i2 in generate_ips_part(parts[1]):
            for i3 in generate_ips_part(parts[2]):
                for i4 in generate_ips_part(parts[3]):
                    yield i1 + "." + i2 + "." + i3 + "." + i4


def generate_ips_part(text):
    if "*" in text:
        start = 0
        end = 255
    elif "[" in text:
        start = int(text[1:-1].split("-")[0])
        end = int(text[1:-1].split("-")[1])
    else:
        yield text
        return

    for i in range(start, end + 1):
        yield str(i)