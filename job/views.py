from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import Job, RequiredSkill, Proposal, Offer, Contract
from .serializer import JobSerializer, SkillsSerializer, JobListSerializer, ProposalSerializer, \
    ProposalListSerializer, ProposalSerializerForPatchingClient, \
    ProposalSerializerForPatchingClientForClose, OfferSerializer, ContractSerializer, \
    OfferSerializerForClose, ContractSerializerForFreelancer, OfferSerializerForUpdate
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from user.models import Freelancer, Client
from django.db.utils import IntegrityError
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q


# views for job

class JobPagination(PageNumberPagination):
    page_size = 10


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_job(request):
    if request.user.is_authenticated:
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            job_client = Client.objects.get(user=request.user)
            serializer.save(job_client=job_client)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("ro'yxatdan o't ")


class JobListApiView(ListAPIView):
    queryset = Job.objects.all()
    pagination_class = JobPagination
    serializer_class = JobListSerializer


@api_view(['GET'])
def get_job(request, pk):
    try:
        job = Job.objects.get(pk=pk)

    except Job.DoesNoteExist:
        return Response({"error": "Job Not Found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = JobSerializer(job)
    return Response(serializer.data)


# views for required_skills

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_skill(request):
    try:
        serializer = SkillsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response([e])


class SkillsListApiView(ListAPIView):
    queryset = RequiredSkill.objects.all()
    serializer_class = SkillsSerializer


# views for proposal

class CreateProposalApiView(APIView):

    def post(self, request):
        post_data = request.data
        user = request.user

        try:
            if request.user.is_authenticated:
                if request.user.user_type == 'freelancer':
                    serializer = ProposalSerializer(data=post_data)

                    if serializer.is_valid():
                        freelancer = Freelancer.objects.get(user=user)

                        serializer.save(freelancer=freelancer, is_active=True)
                        return Response(serializer.data)
                    return Response(serializer.errors)

                else:
                    return Response('you can not do this action')

            else:
                return Response('please signup or signin')

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as i:
            return Response({"error": i})


@api_view(['GET'])
def get_my_proposals(request):
    if request.user.is_authenticated:
        freelancer = Freelancer.objects.get(user=request.user)
        proposal = Proposal.objects.filter(freelancer=freelancer)

        if proposal:
            serializer = ProposalListSerializer(proposal, many=True)
            return Response(serializer.data)
        return Response({"message": "You have not any proposal.!"})
    else:
        Response({"error": "User is not authenticated.!"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def get_proposals_fordetail(request, pk):
    try:
        if request.user.is_anonymous:
            return Response('loging qiling shaxsingiz aniqlanmadi')

        freelancer = Freelancer.objects.get(user=request.user)
        proposal = Proposal.objects.get(pk=pk, freelancer=freelancer)
        serializer = ProposalListSerializer(proposal)

        return Response(serializer.data)

    except Proposal.DoesNotExist:
        return Response({"message": "Proposal Not Found.!"}, status=status.HTTP_404_NOT_FOUND)

    except Freelancer.DoesNotExist:
        return Response({"message": "You Cannot do this action.!"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_proposal(request, pk):
    try:

        freelancer = Freelancer.objects.get(user=request.user)
        proposal = Proposal.objects.get(pk=pk, freelancer=freelancer)

        if proposal:
            proposal.delete()
            return Response({"message": "Proposal was Successfully deleted"})

    except Proposal.DoesNotExist:
        return Response({"error": "Proposal Yo'q xullas (get out here)"},
                        status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
def update_proposal(request, pk):
    try:
        if request.user.is_authenticated:
            if request.user.user_type == 'freelancer':
                freelancer = Freelancer.objects.get(user=request.user)
                proposal = Proposal.objects.get(pk=pk, freelancer=freelancer)

                serializer = ProposalSerializer(proposal, data=request.data)

                if serializer.is_valid():
                    serializer.save(freelancer=freelancer)
                    return Response(serializer.data)
                return Response(serializer.errors)

            else:
                return Response('you can not do this action')

        else:
            return Response('please signup or signin')

    except Proposal.DoesNotExist:
        return Response({"message": "Proposal Not Found"}, status=status.HTTP_404_NOT_FOUND)


# proposal for client

@api_view(['GET'])
def detail_proposal_for_client(request, pk):
    if request.user.is_authenticated:
        if request.user.user_type == 'client':
            try:
                proposal = Proposal.objects.get(pk=pk)
                client = proposal.job.job_client.user

                if client == request.user:
                    proposal.watched = True
                    serializer = ProposalSerializer(proposal)

                    return Response(serializer.data)

                else:
                    return Response('Unauthorized access', status=403)

            except (Proposal.DoesNotExist, Client.DoesNotExist):
                return Response('Proposal or Client not found', status=404)

        else:
            return Response('You cannot perform this action', status=403)

    else:
        return Response('Please signup or signin', status=401)


@api_view(['PATCH'])
def patch_proposal_for_client_for_close_proposal(request, pk):
    if request.user.is_authenticated:
        if request.user.user_type == 'client':
            try:
                proposal = Proposal.objects.get(pk=pk)

                client = proposal.job.job_client.user

                if client == request.user:
                    serializer = ProposalSerializerForPatchingClientForClose(proposal, data=request.data)
                    if serializer.is_valid():
                        serializer.save(is_active=False)
                        return Response(serializer.data)
                    return Response(serializer.errors, status=400)
                else:
                    return Response('Unauthorized access', status=status.HTTP_401_UNAUTHORIZED)

            except (Proposal.DoesNotExist, Client.DoesNotExist):
                return Response('Proposal or Client not found', status=404)

        else:
            return Response('You cannot perform this action', status=403)

    else:
        return Response('Please signup or signin', status=401)


# views for offer

@api_view(['POST'])
def create_offer(request):
    try:
        if request.user.is_authenticated:
            if request.user.user_type == "client":

                serializer = OfferSerializer(data=request.data)
                proposal_data = request.data['proposals']
                proposal = Proposal.objects.get(pk=proposal_data)

                freelancer = proposal.freelancer

                if serializer.is_valid():
                    client = Client.objects.get(user=request.user)
                    serializer.save(client=client, is_active=True, freelancer=freelancer)
                    return Response(serializer.data)
                return Response(serializer.errors)

            else:
                return Response('you cannot do this action', status=status.HTTP_403_FORBIDDEN)

        else:
            return Response('signup or login', status=403)

    except Proposal.DoesNotExist:
        return Response('Proposal Does Not Found ', status=404)


class MyOfferListApiViewForClient(APIView):

    def get(self, request):
        if request.user.is_authenticated:
            try:
                client = Client.objects.get(user=request.user)
                offer = Offer.objects.filter(
                    Q(client=client),
                    Q(is_active=True)
                )

                if offer:
                    serializer = OfferSerializer(offer, many=True)
                    return Response(serializer.data)
                return Response('you have not any offer.!', status=404)
            except (Client.DoesNotExist, Offer.DoesNotExist):
                return Response('Not Found ')
        else:
            return Response('please signup or login', status=401)


# for archive

class MyOfferListApiViewForClientInArchive(APIView):

    def get(self, request):
        if request.user.is_authenticated:
            try:
                client = Client.objects.get(user=request.user)
                offer = Offer.objects.filter(
                    Q(client=client),
                    Q(is_active=False)
                )

                if offer:
                    serializer = OfferSerializer(offer, many=True)
                    return Response(serializer.data)
                return Response('you have not any offer.!', status=404)
            except (Client.DoesNotExist, Offer.DoesNotExist):
                return Response('Not Found ')
        else:
            return Response('please signup or login', status=401)


class MyOfferListApiViewForFreelancer(APIView):

    def get(self, request):
        if request.user.is_authenticated:

            try:
                freelancer = Freelancer.objects.get(user=request.user)
                offer = Offer.objects.filter(
                    Q(freelancer=freelancer),
                    Q(is_active=True)
                )

                if offer:
                    serializer = OfferSerializer(offer, many=True)
                    return Response(serializer.data)

                return Response('you have not any offer.!', status=404)

            except (Freelancer.DoesNotExist, Offer.DoesNotExist):
                return Response('Not Found ', status=404)

        else:
            return Response('please signup or login', status=401)


# for archive

class MyOfferListApiViewForFreelancerInArchive(APIView):

    def get(self, request):
        if request.user.is_authenticated:

            try:
                freelancer = Freelancer.objects.get(user=request.user)
                offer = Offer.objects.filter(
                    Q(freelancer=freelancer),
                    Q(is_active=False)
                )

                if offer:
                    serializer = OfferSerializer(offer, many=True)
                    return Response(serializer.data)

                return Response('you have not any offer.!', status=404)

            except (Freelancer.DoesNotExist, Offer.DoesNotExist):
                return Response('Not Found ', status=404)

        else:
            return Response('please signup or login', status=401)


# close offer for freelancer

@api_view(['GET'])
def close_offer(request, pk):
    if request.user.is_authenticated:
        if request.user.user_type == 'freelancer':
            try:
                offer = Offer.objects.get(pk=pk)
                freelancer = offer.proposals.freelancer.user
                proposals = offer.proposals

                if request.user == freelancer:
                    offer.is_active = False
                    offer.save()

                    proposals.is_active = False
                    proposals.save()

                    offer.save()
                    return Response("offer successfully closed .!")
                else:
                    return Response('you cannot do this action')
            except Offer.DoesNotExist:
                return Response('Offer Not Found', status=404)

        else:
            return Response('you cannot do this action')

    else:
        return Response('you must sign in or register our platform.!', status=403)


# accept offer for freelancer

@api_view(['GET'])
def accept_offer(request, pk):
    try:
        if request.user.is_authenticated:
            if request.user.user_type == 'freelancer':
                offer = Offer.objects.get(pk=pk)

                accept_user = offer.proposals.freelancer.user

                if request.user == accept_user:
                    offer.is_active = False
                    offer.is_accept = True  # test qilinishi kerak

                    offer.proposals.is_active = False
                    offer.proposals.save()

                    offer.save()
                    return Response('offer was accepted.!', status=200)
                else:
                    return Response('you cannot do this action', status=403)

            else:
                return Response('you cannot do this action', status=403)

        else:
            return Response('you must sign in or register our platform.!', status=403)

    except Offer.DoesNotExist:
        return Response('Offer Not Found', status=404)


# offer update view for client
@api_view(['PATCH'])
def offer_update(request, pk):
    try:
        if request.user.is_authenticated:
            if request.user.user_type == 'client':

                client = Client.objects.get(user=request.user)

                offer = Offer.objects.get(pk=pk, client=client)
                proposals = offer.proposals
                freelancer = offer.freelancer
                contract = offer.contract

                serializer = OfferSerializerForUpdate(offer, data=request.data)
                if serializer.is_valid():
                    serializer.save(client=client, proposals=proposals, freelancer=freelancer, contract=contract)
                    return Response(serializer.data)
                return Response(serializer.errors)

            else:
                return Response('you cannot do this action', status=403)

        else:
            return Response('you must sign in or register our platform.!', status=403)

    except Offer.DoesNotExist:
        return Response('Offer Not Found', status=404)


# views for contract

class ContractListApiView(ListAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer


# must be to test

@api_view(['PATCH'])
def sign_contract(request, pk):
    try:
        if request.user.is_authenticated:
            if request.user.user_type == 'freelancer':
                contract = Contract.objects.get(pk=pk)
                user = contract.offer.proposals.freelancer.user

                if request.user == user:
                    serializer = ContractSerializerForFreelancer(contract, data=request.data)
                    if serializer.is_valid():
                        contract.offer.is_accept = True
                        contract.offer.is_active = False
                        contract.offer.save()  # test qilib korish kerak
                        serializer.save()

                        return Response(serializer.data)
                    return Response(serializer.errors)
                else:
                    return Response('you cannot do this action', status=403)

            else:
                return Response('you cannot do this action', status=403)

        else:
            return Response('you must sign in or register our platform.!', status=403)

    except Offer.DoesNotExist:
        return Response('Offer Not Found', status=404)


@api_view(['GET'])
def close_contract(request, pk):
    if request.user.is_authenticated:
        if request.user.user_type == 'freelancer':
            try:
                contract = Contract.objects.get(pk=pk)
                freelancer = contract.offer.freelancer.user

                if request.user == freelancer:
                    contract.offer.is_active = False
                    contract.offer.save()

                    proposal = contract.offer.proposals
                    proposal.is_active = False
                    proposal.save()

                    contract.save()

                    return Response("contract successfully closed .!")
                else:
                    return Response('you cannot do this action')
            except Contract.DoesNotExist:
                return Response('contract Not Found', status=404)

        else:
            return Response('you cannot do this action')

    else:
        return Response('you must sign in or register our platform.!', status=403)


# contract list for client

class MyContractListApiViewForClient(APIView):

    def get(self, request):
        if request.user.is_authenticated:
            try:
                client = Client.objects.get(user=request.user)
                contract = Contract.objects.filter(
                    Q(client=client),
                    Q(offer__is_active=True)
                )

                if contract:
                    serializer = ContractSerializer(contract, many=True)
                    return Response(serializer.data)
                return Response('you have not any contract.!', status=404)
            except (Client.DoesNotExist, Contract.DoesNotExist):
                return Response('Not Found ')
        else:
            return Response('please signup or login', status=401)


# for archive

class MyContractListApiViewForClientInArchive(APIView):

    def get(self, request):
        if request.user.is_authenticated:
            try:
                client = Client.objects.get(user=request.user)
                contract = Contract.objects.filter(
                    Q(offer__client=client),
                    Q(offer__is_active=False)
                )

                if contract:
                    serializer = ContractSerializer(contract, many=True)
                    return Response(serializer.data)
                return Response('you have not any closed contract.!', status=404)
            except (Client.DoesNotExist, Contract.DoesNotExist):
                return Response('Not Found ')
        else:
            return Response('please signup or login', status=401)


# contract list for freelancer

class MyContractListApiViewForFreelancer(APIView):

    def get(self, request):
        if request.user.is_authenticated:
            try:
                freelancer = Freelancer.objects.get(user=request.user)
                contract = Contract.objects.filter(
                    Q(offer__freelancer=freelancer),
                    Q(offer__is_active=True)
                )

                if contract:
                    serializer = ContractSerializer(contract, many=True)
                    return Response(serializer.data)

                return Response('you have not any contract.!', status=404)

            except (Freelancer.DoesNotExist, Contract.DoesNotExist):
                return Response('Not Found ', status=404)
        else:
            return Response('please signup or login', status=401)


# for archive

class MyContractListApiViewForFreelancerInArchive(APIView):

    def get(self, request):
        if request.user.is_authenticated:
            try:
                freelancer = Freelancer.objects.get(user=request.user)
                contract = Contract.objects.filter(
                    Q(offer__freelancer=freelancer),
                    Q(offer__is_active=False)
                )

                if contract:
                    serializer = ContractSerializer(contract, many=True)
                    return Response(serializer.data)

                return Response('you have not any closed contract.!', status=404)

            except (Freelancer.DoesNotExist, Contract.DoesNotExist):
                return Response('Not Found ', status=404)
        else:
            return Response('please signup or login', status=401)
