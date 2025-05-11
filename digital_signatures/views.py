from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import KeyPair, SignatureRecord, VerificationLog, UserActivity
from .ecdsa import initialize_curve, ECDSA, Point
from django.utils import timezone
from .steganography import Steganography
from PIL import Image
import io
import fitz  # PyMuPDF for PDF handling
import numpy as np
from docx2pdf import convert  # For handling Word documents
import tempfile
import os

curve = initialize_curve()
ecdsa = ECDSA(curve)

def index(request):
    return render(request, 'digital_signatures/index.html')

@csrf_exempt
def generate_keys(request):
    if request.method == 'POST':
        try:
            private_key, public_key = ecdsa.generate_keypair()
            key_pair = KeyPair(
                private_key=str(private_key),
                public_key_x=str(public_key.x),
                public_key_y=str(public_key.y)
            )
            key_pair.save()
            
            # Log the key generation activity
            UserActivity.objects.create(
                activity_type='GEN',
                success=True
            )
            
            return JsonResponse({
                'private_key': str(private_key),
                'public_key': {
                    'x': str(public_key.x),
                    'y': str(public_key.y)
                }
            })
        except Exception as e:
            UserActivity.objects.create(
                activity_type='GEN',
                success=False,
                error_message=str(e)
            )
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid method'}, status=405)

def sign_message(request):
    try:
        private_key = request.POST.get('private_key')
        message = request.POST.get('message')
        
        if not private_key or not message:
            return JsonResponse({'error': 'Private key and message are required'}, status=400)

        # Convert private_key to int if necessary
        private_key = int(private_key)

        # Your signing logic here
        signature = ecdsa.sign(message, private_key)
        
        # Save signature record
        key_pair = KeyPair.objects.get(private_key=private_key)
        SignatureRecord.objects.create(
            message=message,
            signature_r=str(signature[0]),
            signature_s=str(signature[1]),
            key_pair=key_pair,
            is_valid=True,
            timestamp=timezone.localtime()  # Use localtime instead of now()
        )
        
        # Log signing activity
        UserActivity.objects.create(
            activity_type='SIGN',
            success=True
        )
        
        return JsonResponse({
            'signature': {
                'r': str(signature[0]),
                's': str(signature[1])
            }
        })
    except ValueError as e:
        return JsonResponse({'error': f'Invalid input: {str(e)}'}, status=400)
    except Exception as e:
        UserActivity.objects.create(
            activity_type='SIGN',
            success=False,
            error_message=str(e)
        )
        return JsonResponse({'error': f'Error signing message: {str(e)}'}, status=500)

@csrf_exempt
def verify_signature(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            public_key_x = int(data.get('public_key_x'))
            public_key_y = int(data.get('public_key_y'))
            public_key = Point(public_key_x, public_key_y)
            message = data.get('message')
            r = int(data.get('r'))
            s = int(data.get('s'))

            is_valid = ecdsa.verify(message, (r, s), public_key)
            
            # Log verification attempt
            VerificationLog.objects.create(
                message=message,
                public_key_x=str(public_key_x),
                public_key_y=str(public_key_y),
                signature_r=str(r),
                signature_s=str(s),
                verification_result=is_valid
            )
            
            # Log activity
            UserActivity.objects.create(
                activity_type='VER',
                success=True
            )
            
            return JsonResponse({'is_valid': is_valid})
        except Exception as e:
            UserActivity.objects.create(
                activity_type='VER',
                success=False,
                error_message=str(e)
            )
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return render(request, 'digital_signatures/verify_signature.html')

@csrf_exempt
def sign_document(request):
    try:
        file = request.FILES.get('file')
        private_key = request.POST.get('private_key')
        message = request.POST.get('message')
        
        if not all([file, private_key, message]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        try:
            # Generate signature
            private_key = int(private_key)
            signature = ecdsa.sign(message, private_key)
            
            # Get public key
            key_pair = KeyPair.objects.get(private_key=str(private_key))
            
            # Prepare data to embed
            embed_data = {
                'message': message,
                'public_key_x': key_pair.public_key_x,
                'public_key_y': key_pair.public_key_y,
                'signature_r': str(signature[0]),
                'signature_s': str(signature[1])
            }
            
            # Convert to string for embedding
            data_string = json.dumps(embed_data)
            
            # Process image and embed data
            img = Image.open(file)
            processed_img, encryption_key = Steganography.embed(img, data_string)
            
            # Save to bytes
            img_byte_array = io.BytesIO()
            processed_img.save(img_byte_array, format='PNG')
            img_byte_array.seek(0)
            
            # Store encryption key in session
            request.session['encryption_key'] = encryption_key.hex()
            
            # Log activity
            UserActivity.objects.create(
                activity_type='SIGN',
                success=True
            )
            
            response = HttpResponse(img_byte_array, content_type='image/png')
            response['Content-Disposition'] = f'attachment; filename="signed_{file.name}"'
            return response
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    except Exception as e:
        UserActivity.objects.create(
            activity_type='SIGN',
            success=False,
            error_message=str(e)
        )
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def verify_document(request):
    try:
        file = request.FILES.get('file')
        if not file:
            return JsonResponse({'error': 'No file provided'}, status=400)

        # Get encryption key from session
        encryption_key = bytes.fromhex(request.session.get('encryption_key', ''))
        
        # Extract and decrypt data
        img = Image.open(file)
        extracted_data = Steganography.extract(img, encryption_key)
        
        try:
            data = json.loads(extracted_data)
            
            # Verify the signature
            public_key = Point(int(data['public_key_x']), int(data['public_key_y']))
            signature_r = int(data['signature_r'])
            signature_s = int(data['signature_s'])
            message = data['message']

            # Check if signature is valid regardless of whether it's forged
            is_valid = ecdsa.verify(message, (signature_r, signature_s), public_key)
            is_forged = data.get('is_forged', False)
            
            # Log verification
            VerificationLog.objects.create(
                message=message,
                public_key_x=data['public_key_x'],
                public_key_y=data['public_key_y'],
                signature_r=data['signature_r'],
                signature_s=data['signature_s'],
                verification_result=is_valid
            )

            return JsonResponse({
                'is_valid': is_valid,  # Return actual validity regardless of forge status
                'message': message,
                'public_key_x': data['public_key_x'],
                'public_key_y': data['public_key_y'],
                'signature_r': data['signature_r'],
                'signature_s': data['signature_s'],
                'is_forged': is_forged  # Include forge status for informational purposes
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'Invalid signature data format'
            }, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def forge_document(request):
    try:
        file = request.FILES.get('file')
        message = request.POST.get('message')
        public_key_x = request.POST.get('public_key_x')
        public_key_y = request.POST.get('public_key_y')
        signature_r = request.POST.get('signature_r')
        signature_s = request.POST.get('signature_s')
        
        if not all([file, message, public_key_x, public_key_y, signature_r, signature_s]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        # Prepare forged data
        embed_data = {
            'message': message,
            'public_key_x': public_key_x,
            'public_key_y': public_key_y,
            'signature_r': signature_r,
            'signature_s': signature_s,
            'is_forged': True  # Optional flag to track forged documents
        }
        
        # Convert to string for embedding
        data_string = json.dumps(embed_data)
        
        # Process image with encryption
        img = Image.open(file)
        processed_img, encryption_key = Steganography.embed(img, data_string)
        
        # Save to bytes
        img_byte_array = io.BytesIO()
        processed_img.save(img_byte_array, format='PNG')
        img_byte_array.seek(0)
        
        # Store encryption key in session for later verification
        request.session['encryption_key'] = encryption_key.hex()
        
        response = HttpResponse(img_byte_array, content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename="forge_signed_{file.name}"'
        return response
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)