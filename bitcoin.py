from cryptos import *
c = Bitcoin(testnet=False)
#c.send("89d8d898b95addf569b458fbbd25620e9c9b19c9f730d5d60102abbabcb72678", "tb1qsp907fjefnpkczkgn62cjk4ehhgv2s805z0dkv", "tb1q95cgql39zvtc57g4vn8ytzmlvtt43skngdq0ue", 5000)
with open('keys.txt', 'r') as f:
	keys = [k.rstrip().split('\t') for k in f.readlines()]

try:

	with open('executed.txt', 'r') as f:
		executedHash = set([x.rstrip() for x in f.readlines()]) 

	print(f"loaded {len(executedHash)} executed tasks")
except:
	executedHash = []


	
try:

	with open('execution.txt', 'r') as f:
		executionHash = set([x.rstrip() for x in f.readlines()]) 
	print(f"loaded {len(executionHash)} execution tasks")
except:
	executionHash= []



for targetHash in executionHash:
	if targetHash in executedHash: continue
	print(f"proccessing {targetHash}")
	try:
		
		value = 0
		fromIndex = None
		fee = 140 * 4
		for i, ak in enumerate(keys):
			addr = ak[0]
			inputs = c.unspent(addr)
			v = sum([i['value'] for i in inputs])
			if v > value:
				value = v
				fromIndex = i
		if value < fee:
			# в этом месте неплохо бы сообщить владельцу о том что у него нет денег на кашельке
			print("мало деняг")
			break
		value -= fee
		addrfrom, keyfrom = keys[fromIndex]
		addrto = keys[(fromIndex + 1) % len(keys)][0]
		#script = "6a20271ef787c7e65e6e0a32a77f21bffdf2c623b61876341a4e52aac7a08dc6ba1e"
		opLen = "%02x" % ((len(targetHash) + 1) // 2)
		script = "6a" + opLen + targetHash
		outs = [{'value': value, 'address': addrto}, {'value': 0, 'script': script}]
		print(f"sending from {addrfrom} ({value} + {fee}) to {addrto} with script {script}")
		tx = c.mktx(inputs, outs)
		stx = c.signall(tx, keyfrom.split(':')[1])
#этот пробел символизирует голову автора v

		print(str(stx))
		sstx = serialize(stx)
		print(sstx)
		c.pushtx(sstx)
		try:

			with open('executed.txt', 'a') as f:
				file.write(targetHash + '\n') 

		except: pass
	except Exception as e:
		print("exception: " + str(e))	




'''
> from cryptos import *
> c = Bitcoin(testnet=True)
> priv = sha256('a big long brainwallet password')
> priv
'89d8d898b95addf569b458fbbd25620e9c9b19c9f730d5d60102abbabcb72678'
> pub = c.privtopub(priv)
> pub
'041f763d81010db8ba3026fef4ac3dc1ad7ccc2543148041c61a29e883ee4499dc724ab2737afd66e4aacdc0e4f48550cd783c1a73edb3dbd0750e1bd0cb03764f'
> addr = c.pubtoaddr(pub)
> addr
'mwJUQbdhamwemrsR17oy7z9upFh4JtNxm1'
> inputs = c.unspent(addr)
> inputs
[{'height': 0, 'tx_hash': '6d7a1b133f5ad2ce77d8980a1c84d7b595e4085d5a4a6d347e8a92df6ffc31f5', 'tx_pos': 0, 'value': 7495, 'address': 'mwJUQbdhamwemrsR17oy7z9upFh4JtNxm1'}, {'height': 0, 'tx_hash': 'e1e7b62e5eb4d399c75649e9256a91f0371268ca265ab9265a433bb263baf2f2', 'tx_pos': 0, 'value': 1866771, 'address': 'mwJUQbdhamwemrsR17oy7z9upFh4JtNxm1'}]
> outs = [{'value': 1000000, 'address': 'tb1q95cgql39zvtc57g4vn8ytzmlvtt43skngdq0ue'}, {'value': sum(i['value'] for i in inputs) - 1000000 - 750 , 'address': 'mwJUQbdhamwemrsR17oy7z9upFh4JtNxm1'}]
outs
[{'value': 1000000, 'address': 'tb1q95cgql39zvtc57g4vn8ytzmlvtt43skngdq0ue'}, {'value': 873516, 'address': 'mwJUQbdhamwemrsR17oy7z9upFh4JtNxm1'}]
> tx = c.mktx(inputs,outs)
> tx
{'locktime': 0, 'version': 1, 'ins': [{'height': 0, 'tx_hash': '6d7a1b133f5ad2ce77d8980a1c84d7b595e4085d5a4a6d347e8a92df6ffc31f5', 'tx_pos': 0, 'value': 7495, 'address': 'mwJUQbdhamwemrsR17oy7z9upFh4JtNxm1', 'script': '', 'sequence': 4294967295}, {'height': 0, 'tx_hash': 'e1e7b62e5eb4d399c75649e9256a91f0371268ca265ab9265a433bb263baf2f2', 'tx_pos': 0, 'value': 1866771, 'address': 'mwJUQbdhamwemrsR17oy7z9upFh4JtNxm1', 'script': '', 'sequence': 4294967295}], 'outs': [{'value': 1000000, 'script': '00142d30807e2513178a791564ce458b7f62d758c2d3'}, {'value': 873516, 'script': '76a914ad25bdf0fdfd21ca91a82449538dce47f8dc213d88ac'}]}
> tx2 = c.signall(tx, priv)
> tx2
{'locktime': 0, 'version': 1, 'ins': [{'height': 0, 'tx_hash': '6d7a1b133f5ad2ce77d8980a1c84d7b595e4085d5a4a6d347e8a92df6ffc31f5', 'tx_pos': 0, 'value': 7495, 'address': 'mwJUQbdhamwemrsR17oy7z9upFh4JtNxm1', 'script': '473044022012ba62de78427811650f868209572404a0846bf60b3a3705799877bb5351827702202bcadc067f5dce01ecf10306e033a905a156aec71d769bcffc0e221a0c91c6030141041f763d81010db8ba3026fef4ac3dc1ad7ccc2543148041c61a29e883ee4499dc724ab2737afd66e4aacdc0e4f48550cd783c1a73edb3dbd0750e1bd0cb03764f', 'sequence': 4294967295}, {'height': 0, 'tx_hash': 'e1e7b62e5eb4d399c75649e9256a91f0371268ca265ab9265a433bb263baf2f2', 'tx_pos': 0, 'value': 1866771, 'address': 'mwJUQbdhamwemrsR17oy7z9upFh4JtNxm1', 'script': '47304402205c9b724d2499f167b9557b8efd13b8b2109ae287b712f2db1d3d46cfc31c71a702201a74bda43116977c4605d499177152afd3965b2fe586f3236053786ef19e96090141041f763d81010db8ba3026fef4ac3dc1ad7ccc2543148041c61a29e883ee4499dc724ab2737afd66e4aacdc0e4f48550cd783c1a73edb3dbd0750e1bd0cb03764f', 'sequence': 4294967295}], 'outs': [{'value': 1000000, 'script': '00142d30807e2513178a791564ce458b7f62d758c2d3'}, {'value': 873516, 'script': '76a914ad25bdf0fdfd21ca91a82449538dce47f8dc213d88ac'}]}
> tx3 = serialize(tx2)
> tx3
'0100000002f531fc6fdf928a7e346d4a5a5d08e495b5d7841c0a98d877ced25a3f131b7a6d000000008a473044022012ba62de78427811650f868209572404a0846bf60b3a3705799877bb5351827702202bcadc067f5dce01ecf10306e033a905a156aec71d769bcffc0e221a0c91c6030141041f763d81010db8ba3026fef4ac3dc1ad7ccc2543148041c61a29e883ee4499dc724ab2737afd66e4aacdc0e4f48550cd783c1a73edb3dbd0750e1bd0cb03764ffffffffff2f2ba63b23b435a26b95a26ca681237f0916a25e94956c799d3b45e2eb6e7e1000000008a47304402205c9b724d2499f167b9557b8efd13b8b2109ae287b712f2db1d3d46cfc31c71a702201a74bda43116977c4605d499177152afd3965b2fe586f3236053786ef19e96090141041f763d81010db8ba3026fef4ac3dc1ad7ccc2543148041c61a29e883ee4499dc724ab2737afd66e4aacdc0e4f48550cd783c1a73edb3dbd0750e1bd0cb03764fffffffff0240420f00000000001600142d30807e2513178a791564ce458b7f62d758c2d32c540d00000000001976a914ad25bdf0fdfd21ca91a82449538dce47f8dc213d88ac00000000'
> c.pushtx(tx3)
'd5b5b148285da8ddf9d719627c21f5cbbb3e17ae315dbb406301b9ac9c5621e5'




> from cryptos import *
> coin = Bitcoin(testnet=True)
> publickeys = ['02e5c473c051dae31043c335266d0ef89c1daab2f34d885cc7706b267f3269c609', '0391ed6bf1e0842997938ea2706480a7085b8bb253268fd12ea83a68509602b6e0', '0415991434e628402bebcbaa3261864309d2c6fd10c850462b9ef0258832822d35aa26e62e629d2337e3716784ca6c727c73e9600436ded7417d957318dc7a41eb']
> script, address = coin.mk_multsig_address(publickeys, 2)
> script
'522102e5c473c051dae31043c335266d0ef89c1daab2f34d885cc7706b267f3269c609210391ed6bf1e0842997938ea2706480a7085b8bb253268fd12ea83a68509602b6e0410415991434e628402bebcbaa3261864309d2c6fd10c850462b9ef0258832822d35aa26e62e629d2337e3716784ca6c727c73e9600436ded7417d957318dc7a41eb53ae'
> address
'2ND6ptW19yaFEmBa5LtEDzjKc2rSsYyUvqA'
> tx = coin.preparetx(address, "myLktRdRh3dkK3gnShNj5tZsig6J1oaaJW", 1100000, 50000)
> for i in range(0, len(tx['ins'])):
    sig1 = coin.multisign(tx, i, script, "cUdNKzomacP2631fa5Q4yHv2fADc8Ueymr5Z5NUSJjVM13igcVJk")
    sig3 = coin.multisign(tx, i, script, "cMrziExc6iMV8vvAML8QX9hGDP8zNhcsKbdS9BqrRa1b4mhKvK6f")
    tx = apply_multisignatures(tx, i, script, sig1, sig3)
> tx
'0100000001e62c0b5434108607f52856bfbcf5093363fbd4789141a661a4c6c8042769ed2001000000fd1d0100483045022100dfc75916f6bb5c5b72a45dea44dbc45b47ba90912efb84680a373acadb3b1212022022dbbd66e4871624609d875bdb592d11335eb4ec49c7b87bb0b8bc76f72f80f30147304402204c38cab196ec0e82a9f65ecba70a0dbf73f49e5886e1000b9bc52894e28fa5c9022007bff3f90bcece19036625806d4d1951a03c256627163f1ac4e76a6ee8eae072014c89522102e5c473c051dae31043c335266d0ef89c1daab2f34d885cc7706b267f3269c609210391ed6bf1e0842997938ea2706480a7085b8bb253268fd12ea83a68509602b6e0410415991434e628402bebcbaa3261864309d2c6fd10c850462b9ef0258832822d35aa26e62e629d2337e3716784ca6c727c73e9600436ded7417d957318dc7a41eb53aeffffffff02e0c81000000000001976a914c384950342cb6f8df55175b48586838b03130fad88ac301224030000000017a914d9cbe7c2c507c306f4872cf965cbb4fe51b621998700000000'
> coin.pushtx(tx)
{'status': 'success', 'data': {'txid': 'b64e19311e3aa197063e03657679e2974e04c02c5b651c4e8d55f428490ab75f', 'network': 'BTCTEST'}}


{'locktime': 0, 'version': 1, 'marker': 0, 'flag': 1, 'witness': [{'number': 2, 'scriptCode': '4730440220027144278bdbe5b1e790dcc8cf83481989ae3f4d1bc71d0db6eadaf2a49b8b5d0220555e59a566a818fb2ac569bbbe21673ce99ecb928a705ad1a9d9cd2836fb86fe012102039c196ea18da94b29dd96fe479521fc4a702343b053b5fe3761c20be92a8a7d'}], 'ins': [{'tx_hash': 'e61dbe0cc498059fbcc478598053fd373bbc5236e4d03c431c579634093eef18', 'tx_pos': 0, 'height': 871371, 'value': 3040, 'address': 'bc1q2g63qejx59e8r9t54cgm56v4yzp9g8pdfxnw07', 'script': '', 'sequence': 4294967295}], 'outs': [{'value': 0, 'script': '0014dbe2484b4a3eaeef671db319d1ed6db0e1055247'}, {'value': 2541, 'script': '00145235106646a172719574ae11ba69952082541c2d'}]}

'''
