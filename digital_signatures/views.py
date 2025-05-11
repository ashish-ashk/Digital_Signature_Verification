from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import KeyPair, SignatureRecord, VerificationLog, UserActivity
from .ecdsa import initialize_curve, ECDSA, Point
from django.utils import timezone

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