import vk_api


def authorization():
    vk_session = vk_api.VkApi(token='ec893kbs820d9182968f48b8c434cbc384fdfue34gh4432jf744706d872e34b8e40e52d90ado02c3')
    return vk_session
