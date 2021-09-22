from pyats.topology import loader

testbed = loader.load('testbed_sr.yaml')

ios_1 = testbed.devices['Paris-26']

# establish basic connectivity
ios_1.connect(log_stdout=False)

# issue commands
show_interface = ios_1.learn('interface')

for interface, info in show_interface.info.items():

    # Step 4: What if the key 'ipv4' doesn't exist (= no assigned IPv4)?
    if 'ipv4' in info:
        for ip, value in info['ipv4'].items():
            ip = value.get('ip', "NA")
            print(f'{interface} -- {ip}')
    else:
        print(f'{interface} -- Unassigned')

print('')
ios_1.disconnect()