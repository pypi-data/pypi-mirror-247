import json
import blockcypher # will be replace by px_blockcypher in the future
from bitcoinlib.wallets import Wallet
from bitcoinlib.wallets import WalletError
from bitcoinlib.wallets import HDKey
from bitcoinlib.wallets import WalletKey
from bitcoinlib.keys import BKeyError


class PxValueError(ValueError):
    """
    Handle PxWallet class value Exceptions
    
    """
    pass

class PxKeyError(BKeyError):
    """
    Handle PxWallet class Exceptions for Keys

    """
    pass
class PxWalletError(PxValueError):
    """
    Handle PxWallet class Exceptions

    """
    def __init__(self, msg=''):
        self.msg = msg
        super.__init__(msg)

    def __str__(self):
        return self.msg
    

class PxBlockcypherResponseError(PxWalletError):
    """
    Handle PxWallet class Exceptions for (Blockcypher Request-Response Exception)

    """
    def __init__(self, msg=''):
        self.msg = msg
        super.__init__(msg)

    def __str__(self):
        return self.msg
    
    
class PxWallet:
    def __init__(self, _token: str, _wallet_name: str, _extended_key_to_import: str, _is_extended_key_private: bool = False, _printLog: bool = False ):
        self.token = _token
        self.wallet_name = _wallet_name
        self.extended_key_to_import = _extended_key_to_import
        self.is_extended_key_private = _is_extended_key_private
        self.printLog=_printLog

    def create_blockcypher_hd_wallet(self):
        """
        This method create a wallet on BlockCypher Service by sending an HTTP request to the hd wallet endpoint and as well create a internal wallet which can be use to manage/retrieve addresses, public & private keys info.  
        
        @author: Prince Foli (developer.prncfoli@gmail.com)

        @return ``dict[str, Any]``:  There are 3 main dictionary key of interest here. These are ``blockcyper_wallet_response``, ``internal_wallet_info``, ``imported_key_info``
        
        NB:

        required library: ``blockcypher`` , ``bitcoinlib`` 
        
        use the command below to install:

        ``pip3 install blockcypher bitcoinlib``

        """

            
        if  not (self.token and self.token.strip()):
            raise PxValueError("Blockcypher token is required")
        
        if not (self.wallet_name and self.wallet_name.strip()):
            raise PxValueError("blockcypher wallet name is required")
        
        if not (self.extended_key_to_import and self.extended_key_to_import.strip()):
            raise PxValueError("extended_key_to_import ( zpub or zprv - Account level key ) is required")
        
        if not (self.extended_key_to_import.startswith("zpub") or  self.extended_key_to_import.startswith("zprv")):
            raise PxValueError("extended_key_to_import must either begin with zpub or zprv (Account level key)")
        try:
                # depth: 3, is_pivate = true (private), name="Account Extended Private Key"
                imported_key = HDKey.from_wif(self.extended_key_to_import, "bitcoin")
                wif = imported_key
                
                blockcyper_wallet_response = blockcypher.create_hd_wallet( self.wallet_name, xpubkey=imported_key.wif_public(), api_key=self.token, subchain_indices = [0,1], coin_symbol= 'btc' )
                
                if ( str(blockcyper_wallet_response).lower().__contains__('extended_public_key') and  str(blockcyper_wallet_response).lower().__contains__('chains') ):
                    
                    # internal version hd wallet
                    internal_wallet = Wallet.create( self.wallet_name, wif, witness_type='segwit', network='bitcoin' )
                    
                    if( self.printLog ):
                        print(f"[Imported Key info]\n{ imported_key.as_json(include_private=self.is_extended_key_private) }\n" )
                        print(f"[Internal Wallet created with Imported Key]\n{internal_wallet.as_json()}\n\n" )
                        print(f'[Blockcypher create-wallet request\'s response]\n{blockcyper_wallet_response}\n\n' )
                    
                    return  { 
                        "blockcyper_wallet_response": blockcyper_wallet_response, 
                        "internal_wallet_info": internal_wallet.as_json(),
                        "imported_key_info": imported_key.as_json(include_private=self.is_extended_key_private)
                    }
                
                elif( str(blockcyper_wallet_response).lower().__contains__('wallet exists') ):
                    raise PxBlockcypherResponseError(blockcyper_wallet_response['error'])  
                
                else:
                    raise PxBlockcypherResponseError(blockcyper_wallet_response)  
                
        except BKeyError as err:
            print(f"%s" %(err.msg))

        except WalletError as err:
            if (err.msg):
                print(f"%s" %(err.msg))
               
        except Exception as err:
            if (err.args):
                print(f"%s" %(err))

    def create_blockcypher_hd_wallet_with(self, subchain_indices=[0,1] ):
        """
        This method create a wallet on BlockCypher Service by sending an HTTP request to the hd wallet endpoint and as well create a internal wallet which can be use to manage/retrieve addresses, public & private keys info.  
        learn more about chains here https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki#change
        @author: Prince Foli (developer.prncfoli@gmail.com)

        @param ``subchain_indices``: these indices indicates the address chain type that you want to create, where 0 is normal address chain and 1 is change address chain.
        @return ``dict[str, Any]``:  There are 3 main dictionary key of interest here. These are ``blockcyper_wallet_response``, ``internal_wallet_info``, ``imported_key_info``
        
        NB:

        required library: ``blockcypher`` , ``bitcoinlib`` 
        
        use the command below to install:

        ``pip3 install blockcypher bitcoinlib``

        """

            
        if  not (self.token and self.token.strip()):
            raise PxValueError("Blockcypher api token is required")
        
        if not (self.wallet_name and self.wallet_name.strip())  :
            raise PxValueError("wallet name is required")
        
        if not (self.extended_key_to_import and self.extended_key_to_import.strip())  :
            raise PxValueError("extended_key_to_import is required")
        
        if not (self.extended_key_to_import.startswith("zpub") or  self.extended_key_to_import.startswith("zprv")):
           raise PxValueError("extended_key_to_import must either begin with zpub or zprv")
        
        
        try:
            
            # depth: 3, is_pivate = true (private), name="Account Extended Private Key"
            imported_key = HDKey.from_wif(self.extended_key_to_import,"bitcoin")
            wif = imported_key
                
            blockcyper_wallet_response = blockcypher.create_hd_wallet( self.wallet_name, xpubkey=imported_key.wif_public(), api_key=self.token, subchain_indices=subchain_indices , coin_symbol= 'btc' )
                
            if ( str(blockcyper_wallet_response).lower().__contains__('extended_public_key') and  str(blockcyper_wallet_response).lower().__contains__('chains') ):
                    
                internal_wallet = Wallet.create( self.wallet_name, wif, witness_type='segwit', network='bitcoin' )
                    
                if( self.printLog ):
                    print(f"[Imported Key info]\n{ imported_key.as_json(include_private=self.is_extended_key_private) }\n" )
                    print(f"[Internal Wallet created with Imported Key]\n{internal_wallet.as_json()}\n\n" )
                    print(f'[Blockcypher create-wallet request\'s response]\n{blockcyper_wallet_response}\n\n' )
                
                return  { 
                    "blockcyper_wallet_response": blockcyper_wallet_response, 
                    "internal_wallet_info": internal_wallet.as_json(),
                    "imported_key_info": imported_key.as_json(include_private=self.is_extended_key_private)
                }
                
            elif( str(blockcyper_wallet_response).lower().__contains__('wallet exists') ):
                raise PxBlockcypherResponseError(blockcyper_wallet_response['error'])  
                
            else:
                raise PxBlockcypherResponseError(blockcyper_wallet_response)  
                

        except BKeyError as err:
            print(f"%s" %(err.msg))

        except WalletError as err:
            if (err.msg):
                print(f"%s" %(err.msg))

        except Exception as err:
            if (err.args):
                print(f"%s" %(err))

    @staticmethod
    def retrieve_blockcypher_hd_wallet_addresses( _wallet_name: str = None, _token: str = None):
        """
        This method retrieves blockcypher hd wallet addresses that has been already derived and perharbs used. It does this by making a HTTP request to Blockblockcypher Server.
        """
        if  not (_token and _token.strip()):
            raise PxValueError("Blockcypher api token is required")
        
        if not (_wallet_name and _wallet_name.strip())  :
            raise PxValueError("wallet name is required")
      
        try:
            blockcypher_retrieved_addresses_response = blockcypher.get_wallet_addresses( _wallet_name, api_key=_token, is_hd_wallet=True, coin_symbol= 'btc')
           
            return blockcypher_retrieved_addresses_response
              
        except WalletError as err:
            if (err.msg):
                print(f"Error: {err.msg}")

        except Exception as err: 
            if (err):
                print(f"Unexpected Error {err=}, {type(err)=}")
    

    @staticmethod
    def retrieve_internal_hd_wallet( _wallet_name: str = None):
        """
          Retrives the internal wallet reference that enable you to handle public & private key operation from the wif (private) imported.\
          The operation such as retrieving public key, private key and its corresponding addresses with a given `sub chain index` (a.k.a change) and `address index`.
        """
       
        if not (_wallet_name and _wallet_name.strip())  :
            raise PxValueError("wallet name is required")
      
        try:

            internal_wallet = Wallet(_wallet_name)
            return internal_wallet

        except WalletError as err:
            if (err.msg):
                #print(f"Error: {err.msg}")
                raise PxWalletError(err.msg)        

        except Exception as err: 
            if (err):
                #print(f"Unexpected Error {err=}, {type(err)=}")
                raise Exception(f"Unexpected error.\n{err=}, {type(err)=}")
    
   
    @staticmethod
    def retrieve_internal_hd_wallet_key_for_path_with( _wallet_name: str = None, subchain_index: int = 0, address_index: int = 0 ):
        """
          Retrives the internal wallet reference that enable you to handle public & private key operation from the wif (private) imported.\
          The operation such as retrieving public key, private key and its corresponding addresses with a given `subchain_index` (a.k.a change) and `address_index`.  When `subchain_index` is not provided, a default subchain_index `0` will be used and also when `address_index` is not provided, a default address_index `0` will be used.
        """
       
        if not (_wallet_name and _wallet_name.strip())  :
            raise PxValueError("wallet name is required")
      
        try:

            internal_wallet = Wallet(_wallet_name)
            internal_wallet_key: WalletKey = internal_wallet.key_for_path(([subchain_index, address_index]))
            key_info = json.loads('{"wif": "%s", "private_hex":"%s", "private_bytes":"%s", "public_hex":"%s", "public_bytes":"%s",  "public_compressed_hex":"%s",  "public_compressed_bytes":"%s"  }' %( internal_wallet_key.key().wif_key(), internal_wallet_key.key().private_hex,  internal_wallet_key.key().private_byte, internal_wallet_key.key().public().public_hex,  internal_wallet_key.key().public().public_byte,  internal_wallet_key.key().public().public_compressed_hex,  internal_wallet_key.key().public().public_compressed_byte  ))
           
            return (key_info, internal_wallet_key )
        
        except BKeyError as err:
            if (err.msg):
                #print(f"Error: {err.msg}")
                raise PxKeyError(err.msg)

        except WalletError as err:
            if (err.msg):
                #print(f"Error: {err.msg}")
                raise PxWalletError(err.msg)        

        except Exception as err: 
            if (err):
                #print(f"Unexpected Error {err=}, {type(err)=}")
                raise Exception(f"Unexpected error.\n{err=}, {type(err)=}")

    @staticmethod
    def retrieve_internal_hd_wallet_key_for_path( _wallet_name: str = None, path: str = "m/0/0"  ):
        """
          Retrives the internal wallet reference that enable you to handle public & private key operation from the wif (private) imported.\
          The operation such as retrieving public key, private key and its corresponding addresses with a given `path`. For example if `path="m/i/j"` where  `i` is the `subchain_index` (a.k.a change) and `j` is the `address_index`. When `path` is not provided, it will return a key for default path. Thus `m/0/0`.
        """
       
        if not (_wallet_name and _wallet_name.strip()):
            raise PxValueError("wallet name is required")
        
        if not ( path and path.strip()):
            raise PxValueError(" key/address path is required")
        
        if not (isinstance(path, str)):
            raise PxValueError("key/address must be of type str")
        
        if not (  path.__contains__('/') and len(path.lower().split('/')) == 3 and path.lower()[0] == 'm' ):
            raise PxValueError("key/address must a valid path. For example: m/0/1, where 0 is `subchain_index` (a.k.a change level) and 1 is the address_index")
      
        try:

            internal_wallet = Wallet(_wallet_name)

            _pathSplit = path.lower().split('/')
            internal_wallet_key: WalletKey = internal_wallet.key_for_path(([int(_pathSplit[1]), int(_pathSplit[2])]))
            
            key_info = json.loads('{"wif": "%s", "private_hex":"%s", "private_bytes":"%s", "public_hex":"%s", "public_bytes":"%s",  "public_compressed_hex":"%s",  "public_compressed_bytes":"%s"  }' %( internal_wallet_key.key().wif_key(), internal_wallet_key.key().private_hex,  internal_wallet_key.key().private_byte, internal_wallet_key.key().public().public_hex,  internal_wallet_key.key().public().public_byte,  internal_wallet_key.key().public().public_compressed_hex,  internal_wallet_key.key().public().public_compressed_byte  ))
            return (key_info, internal_wallet_key )
        
        except BKeyError as err:
            if (err.msg):
                #print(f"Error: {err.msg}")
                raise PxKeyError(err.msg)

        except WalletError as err:
            if (err.msg):
                #print(f"Error: {err.msg}")
                raise PxWalletError(err.msg)        

        except Exception as err: 
            if (err):
                #print(f"Unexpected Error {err=}, {type(err)=}")
                raise Exception(f"Unexpected error.\n{err=}, {type(err)=}")



        
class PxWalletKeyGenerator:
    @staticmethod
    def generate_seed_phrase(print_log=True):
        
        """
        This generate 12 word phrase that can serve as a recovery phrase (word list). This word list is supposed to be kept secret. Please do not share this with anyone because doing so will mean you are giving away your private key info. Only use it to recover funds on any trusted wallet or wallet provider service or application. Please note that not keeping your ``seed``  or ``secret_recovery_words``safe may result you losing your funds. 
        
        @author: Prince Foli (developer.prncfoli@gmail.com)

        @return ``tuple[str, dict[str, Any]]``:  The first index of tuple is ``recovery phrase`` which is also known as ``seed phrase`` or ``backup phrase``. The second index of the tuple is dictionary of ``seed`` values. There are two main dictionary keys that might be of interest. These are ``bytes`` and ``hex`` and they represent the format of the seed
        
        NB:

        required library: ``mnemonic`` 
        
        use the command below to install:

        ``pip3 install mnemonic``
        """

        from mnemonic import Mnemonic

        mnemo = Mnemonic("english")
        
        # word count: [ 12,  15,  18,  21,  24]
        # bit size:   [128, 160, 192, 224, 256]
        secret_recovery_words = mnemo.generate(strength=128)
        if (print_log):
            print('\n[Secret Recovery Phrase | Backup Phrase | Seed Phrase]\n\n%s\n\n' %secret_recovery_words)

        master_seed = mnemo.to_seed(secret_recovery_words, passphrase="")
        if (print_log):
            print('[ Seed (in hex) ]\n\n%s\n' %master_seed.hex())
        seed = { "hex":  (master_seed.hex()), "bytes": master_seed }
        return ( secret_recovery_words, seed )
    
    @staticmethod
    def seedToMasterKey(seed, print_log=True):
    
        """
        Import/Retrieve segwit extended master key from ``seed`` (in hex)

        @author: Prince Foli (developer.prncfoli@gmail.com)

        @type ``seed``: hex
        @param ``seed``: The seed (in hex) to import.

        @return ``(tuple[dict[str, dict[str, Any]], HDKey] | None)``: The first index of tuple is dictionary that contains master key information and the second index is the HDKey object of the master key. There are two main dictionary key that is of interest and these are ``extended_key`` and ``account_keys``. Note that these are all extended keys but serve different roles. ``Account Keys`` (``account_keys`` because their ``depth`` equals ``3``) are normally derived from ``Root Extended Keys`` ( ``extend_keys`` a.k.a ``root keys`` because their ``depth`` equals ``0`` ).
        
        # usage: 

        >>> recovery_words, seed = PxWalletKeyGenerator.generate_seed_phrase()

        >>> info, key = PxWalletKeyGenerator.seedToMasterKey(seed['hex'])


        # NB: 
        
        ``Extended private key (xprv, zprv)`` = ``Parent private key``   ``+``   ``Parent chain code`` 
        
        ``Extended public key (xpub, zpub)`` = ``Parent public key``   ``+``   ``Parent chain code`` 

        The first level extended private key generated is also known as ``BIP32 Root key`` or ``Master (private) key`` 
        
        The first level extended public key generated is also known as  ``BIP32 Root key`` or ``Master (public) key``
        
        required library: ``bitcoinlib`` 
        
        use the command below to install:
        
        ``pip3 install bitcoinlib``
        """
        from bitcoinlib.wallets import HDKey
        
        if (seed is None):
            raise PxValueError('seed parameter is required')
        else:
            master_key_info = HDKey.from_seed(seed, encoding='bech32', witness_type='segwit', network='bitcoin')
            if(master_key_info):
                point_x, point_y = master_key_info.public_point()
                if (master_key_info.secret):
                    key_info = {
                        "master_key_info": { 
                            "network": "%s" %master_key_info.network.name,
                            "bip32_root_key": "%s" %master_key_info.wif(is_private=True),
                            "extended_keys": [
                                {
                                    "name": "extended_private_key",
                                    "value": "%s" %master_key_info.wif(is_private=True),
                                    "depth": 0,
                                    "format": "wif",
                                    "note": "This is the BIP32 root private key. It is also known the root key. This is same as ``bip32_root_key`` "
                                },
                                {
                                    "name": "extended_public_key",
                                    "value": "%s" %master_key_info.wif_public(),
                                    "depth": 0,
                                    "format": "wif",
                                    "note": "This is the BIP32 root public key "
                                }
                            ],
                            "account_keys": {
                                "zpub":  "%s" %master_key_info.subkey_for_path("m/84'/0'/0'").wif_public(),
                                "zprv":  "%s" %master_key_info.subkey_for_path("m/84'/0'/0'").wif_private(),
                                "format": "wif",
                                "path": "m/84'/0'/0'",
                                "depth": 3,
                                "note": "These keys are known as account level keys because they are derived on the path ``m/84'/0'/0'``. The path representation is ``m/purpose/coin_type/account``. Keys derived on path is also known as ``Segwit as root key``."
                            },
                            "parent": {
                                "private":[
                                    { 
                                        "name": "parent_private_key_wif",
                                        "key": "%s" %master_key_info.wif_key(),
                                        "format": "wif"
                                    },
                                    { 
                                        "name": "parent_private_key_hex",
                                        "key": "%s" %master_key_info.private_hex,
                                        "format": "hex",
                                        "compressed": True,
                                    },
                                    { 
                                        "name": "parent_secret",
                                        "key": "%s" %master_key_info.secret,
                                        "format": "long", 
                                    },
                                ],
                                "public":[
                                    { 
                                        "name": "public_key_hex",
                                        "key": "%s" %master_key_info.public_hex,
                                        "format": "hex",
                                        "compressed": True,
                                    },
                                    { 
                                        "name": "public_key_uncompressed_hex",
                                        "key": "%s" %master_key_info._public_uncompressed_hex,
                                        "format": "hex",
                                        "compressed": False,
                                    },
                                    { 
                                        "name": "hash160_hex",
                                        "key":  "%s" %master_key_info.hash160.hex(),
                                        "format": "hex" 
                                    },
                                    { 
                                        "name": "hash160_bytes",
                                        "key": "%s" %master_key_info.hash160,
                                        "format": "bytes",
                                    }
                                ],
                                "public_key_points": {
                                    "x": "%s" %point_x,
                                    "y" : "%s" %point_y ,
                                },
                                "address" : {
                                    "value": "%s" %master_key_info.address(),
                                    "type": "segwit",
                                    "format": "bech",
                                    "note": 'bc1 address'
                                },
                                "chain": {
                                    "name":"parent_chain_code",
                                    "code": "%s" %master_key_info.chain.hex(),
                                    "format": "hex"
                                }
                            }
                        } 
                    }
                    
                    if(print_log):
                        # master_key_info.info()
                        print('\n[key_info]\n\n%s\n' %key_info, sep='') 
                    return (key_info , master_key_info)
     

