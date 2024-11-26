#!/usr/bin/env python3
import requests
import json


def get_transactions(address):
	url = f"https://blockchain.info/address/{address}?format=json"          
	response = requests.get(url)

	if response.status_code == 200:
		transaction_data = response.json()
		return transaction_data
	else:
		print(f"Error: {response.status_code}")
		return None

def get_script_hash_via_www(transID):

        def get_transaction_data(txid):
            url = f"https://blockchain.info/rawtx/{txid}?format=json"
            response = requests.get(url)

            if response.status_code == 200:
                transaction_data = response.json()
                return transaction_data
            else:
                print(f"Error: {response.status_code}")
                return None

        transaction_data = get_transaction_data(transID)
        output = transaction_data["out"]

        for current in output:
                if "addr" not in current and "script" in current:
                        script = current["script"]
                        if transaction_data:
                                 #print(f"данные транзакции: {json.dumps(transaction_data, indent=4, ensure_ascii=False)}")
                                 #print(f"данные транзакции: {json.dumps(current, indent=4, ensure_ascii=False)}")
                                 return script

#transID = "484ab0edc347949771bf6a2f6be984141531f274d66a30a5e6d9e1a86af9aa39"
#addresses = ["bc1q2g63qejx59e8r9t54cgm56v4yzp9g8pdfxnw07", "bc1qm03ysj6286hw7ecakvvarmtdkrss25j8haw7p6"]
addresses = ["bc1qm03ysj6286hw7ecakvvarmtdkrss25j8haw7p6"]

txset = set()

with open('info.txt', 'r') as file:
	for line in file.readlines():
		line = line.rstrip('\n')
		txset.add(line)	


for addr in addresses:
	data = get_transactions(addr)
	#print(str(result))
	#data = json.loads(result)
	txs = data.get('txs', None)
	if txs is None: continue
	for tx in txs:
		output = tx.get("out", [])

		for current in output:
			if "addr" not in current and "script" in current:
				script = current["script"]
				print(script)
				print(str(tx))
				#fieldnames = ['hashid', 'transid', 'time', 'op_return', 'comment']
				transid = tx.get('hash', '')
				timestamp = str(int(tx.get('time', '')) // 60 * 60)
				op_return = script
				if not op_return.startswith('6a'): continue
				datalen = int(op_return[2:4], 16)
				if datalen < 32: continue
				hashNcomment = op_return[4:]
				hashid = hashNcomment[:64]
				byte_array = bytes.fromhex(hashNcomment[64:])
				comment = byte_array.decode('utf-8')
				formatout = f"{hashid}\t{transid}\t{timestamp}\t{op_return}\t{comment}"	
				
				if formatout not in txset: 
					with open('info.txt', 'a') as file:
						file.write(formatout + '\n')
						txset.add(formatout)	
						print(formatout)

#{'hash': '484ab0edc347949771bf6a2f6be984141531f274d66a30a5e6d9e1a86af9aa39', 'ver': 2, 'vin_sz': 1, 'vout_sz': 2, 'size': 234, 'weight': 609, 'fee': 644, 'relayed_by': '0.0.0.0', 'lock_time': 870858, 'tx_index': 2029007735692347, 'double_spend': False, 'time': 1731930115, 'block_index': 870868, 'block_height': 870868, 'inputs': [{'sequence': 4294967293, 'witness': '0247304402206c96da9c476a0c219c468fd6aec3d46353fd984f1b54799c087ae90106487f9a02204ff34b886c019e5e608e7b0d2a72788e31ae1d8bb6f261c5059c6fd560e89346012102039c196ea18da94b29dd96fe479521fc4a702343b053b5fe3761c20be92a8a7d', 'script': '', 'index': 0, 'prev_out': {'type': 0, 'spent': True, 'value': 4124, 'spending_outpoints': [{'tx_index': 2029007735692347, 'n': 0}], 'n': 5, 'tx_index': 6370486307463280, 'script': '00145235106646a172719574ae11ba69952082541c2d', 'addr': 'bc1q2g63qejx59e8r9t54cgm56v4yzp9g8pdfxnw07'}}], 'out': [{'type': 0, 'spent': False, 'value': 0, 'spending_outpoints': [], 'n': 0, 'tx_index': 2029007735692347, 'script': '6a20648f1f1f7d696316c654c6e6165748bb80a0f6d09be72fcbb081487d7b9fc345'}, {'type': 0, 'spent': True, 'value': 3480, 'spending_outpoints': [{'tx_index': 877306145313482, 'n': 0}], 'n': 1, 'tx_index': 2029007735692347, 'script': '0014dbe2484b4a3eaeef671db319d1ed6db0e1055247', 'addr': 'bc1qm03ysj6286hw7ecakvvarmtdkrss25j8haw7p6'}], 'result': 3480, 'balance': 3480}

#raise Exception ("этот скрипт не учитывает номер команды и длину записи, которые пишутся перед хэшем")
#
#with open('info.txt', 'a') as file:
#    # Добавляем строки в файл
#    file.write(get_script_hash_via_www(transID) + '\n')
#    file.write(' \n')
