def ex_qotp(backend, host):

    print(host)
    print(backend.PREP(host))
    
    clear_block = [backend.PREP(host) for i in range(10)]
    flip_block = [random.randint(0,1) for i in range(10)]

    for q,k in zip(clear_block, flip_block):
        if k == 1: backend.X(q)

    print('Clear block')
    qr.display(clear_block)
    
    print('## Applying QOTP')
    enc_block, key = zip(*qr.qotp_enc(clear_block))

    #print('Encrypted block') 
    #qr.display(enc_block)
    #print('Used key')
    #print(key)

    print('## Decripting')
    dec_block = list(qr.qotp_dec(enc_block, key))
    print('Decrypted block') 
    qr.display(dec_block)
        
def ex_stream(backend, sourcehost, targethost):
    block = [backend.PREP(sourcehost) for i in range(10)]
    print('Preparation done, checking qubit host')
    qr.display(block)
    qr.stream(block, targethost)
    print('Send done, checking qubit host')
    qr.display(block)
