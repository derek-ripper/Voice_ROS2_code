# Filename: gcp_credentials.py
# Created : 15 Aug 2017
# Author  : Derek Ripper
# Purpose : Contains 2 sets of GCP(google cloud platform) credentials using 2
#           independent "google service accounts".
#           Set up to falcilitate use of google "cloud speech recogintion API"
#           Used by s2t.py

def gcp_credentials(keyowner): 

   if keyowner == "Zeke" : # Zeke?
	   credentials = r"""{
	  "type": "service_account",
	  "project_id": "gcp-sr",
	  "private_key_id": " ",
	  "private_key": "",
	  "client_email": "",
	  "client_id": "",
	  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
	  "token_uri": "https://accounts.google.com/o/oauth2/token",
	  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
	  "client_x509_cert_url": ""
	}
	"""
   elif keyowner == "Derek" : # Derek?
	   credentials = r"""{
  "type": "service_account",
  "project_id": "gcp-sr",
  "private_key_id": "aa385b5e2f487b3b6adea1210428934506bef0a1",
  "private_key": "-----BEGIN PRIVATE KEY-----\n MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDv0cxm0Bdl+qJe\nqh16Jahj4lCLE8S5k38rj8iBKSurn3hYRtOdUfhwBwKXB1PpYoM2VS4L28nSdklt\n09AW1ogiEVa4z8MxRAUySJlRomEtINfZqVkFTLSOtppMtmML+WpktIVmRDJuQmxG\nLmn6LldFINuDWNheAwMmP+hjHiEu2A3ihImc7J2zt4tCTeQNC/39Z9jugegmBQZs\nww4AbXuB37Z71JK+mUvvZPv+h+gg2GSrgJKM9sH3543CZplcvRLseAjPWTDItRpy\nxOPDB9Y6wWVus3P3cB0NGLOSXKNLXFwFthHazrOQKzORiSK/j25XYlipz+Ruhm6k\nC3nb019bAgMBAAECggEATUyOWcVRBWnX1DN49NoWgLt9wpZInphQMTZTJm6iyNrJ\n64pIwzicn19jElMmVN+P839ZLDFXyCKgYGoZdIMJthFopoExJTwLgL2tzYZNVEJ1\n0I6pRvAGcsmgyoEvQ7jM9lDJfsEUkD2QsL5dImq1bm680oVcmFDYPwfyW6BmibYy\nZnHTfgKr5o3MXAoB+C9Y0LV/TQSkSfldTAVTko3i66rZ88gta5mCE5J+oYSbc9nb\nNUGRW2CW//GKWwMw3aRqoF+so3xJzy7+tRXWeC37pjyma5MDYRMs5rkWAFdxig4b\nfwFHDynwtJ3ZHoIZzZmnaBu0yW2/dJtZrlP1zlf8YQKBgQD6PsDywlr91hB7OLe1\n0HlGSvDZOFVfIWuvjGDr4ol6xHYXVEO7niHWcvl8y9qj2agn4W/+Vp46jYGWfiwC\nanjKhXNWAw+k57g7MfAufgN/De5tMxfB0Y46RFi+16Lg8WluCR/dxbrL4fuKkQ63\nK/6GQm4mCaaV0Yh5QYBZh6WJVQKBgQD1Vaq/CsaiOe3+5zy3+lbi786YIxl37D6B\nOjm1oTGLzDmDow5USy/KpQkc8Agx/0h8mBOyvZG/+vI6AsSZ8RZ4VdSAWFJ/q10r\nmfiV4aLoEPJsIqygZ6IE/CiOxIx1ykV3A47PZJ0893NPqCo82Xl7CemFsvzYHDTm\n96J9bDOF7wKBgHYm8PTtnQaibo+vXNXkQ45TzdnRxkUvQ2fUUOKuyBiF7/fd2kkY\nRYO6L1+j5GxeVQ3XXAhrHzQoIdpLYj4VxUhhr+4ZbeZ/XbXdQzjAWKhBjKRUblAd\nwBh0sq4QpB+u/AdvGXOday/eV+S5zoffpsH/VYByKAwurVALBC3BZQAtAoGBAIsS\nsAMyOZ221xpbvQjSCbUFmgiWRRa9PkWFWzeCFBMahzP/F91i7cmjOoJD83FcNJwk\nnW4Cln/M4slNzmMxzroSda734nRrERrpYoicavvAt5vjIBaiCK9ovhkIhFM1gaFQ\nzAD3GUd5Qs3SF3d9FKdR3CYla72aZ8bSdDNDRgXTAoGAH3qx/xg4VEi7Y+47SUOg\nDBJvVv4bmk5pf+JCB3nwz8XANoJLwXTdTMkFiKkxJLowpRSQ7thisbIY1ksbjNm6\n9idr+/pyHPPHpEoEwrrD6H1Fil4p/6gyyGcehHLsnP5AIGAtJoxeTTIJAU227brz\nfjh1Xgv254Dkp5BVdzNOlZI=\n-----END PRIVATE KEY-----\n",
  "client_email": "derek-752@gcp-sr.iam.gserviceaccount.com",
  "client_id": "103420411461651475926",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://accounts.google.com/o/oauth2/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/derek-752%40gcp-sr.iam.gserviceaccount.com"
	}
	"""
   else:
         print("User for GCP has not been set. Missing User is: "+keyowner)

   return credentials  
