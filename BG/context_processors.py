def user_context(request):
    user = request.user
    return {'user': user}

