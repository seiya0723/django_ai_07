from django.shortcuts import render,redirect
from django.views import View

#ビュークラスに継承させることで、認証状態をチェックする
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Design
from .forms import DesignForm

import magic

ALLOWED_MIME    = [ "image/vnd.adobe.photoshop","application/pdf","application/postscript" ]

class illustView(View):

    def get(self, request, *args, **kwargs):

        #Designクラスを使用し、DBへアクセス、データ全件閲覧
        designs = Design.objects.all()

        button1     = "Prev"
        data        = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        category    = "カテゴリ−１"
        category2   = "カテゴリ−2"
        category3   = "カテゴリ−3"

        context = {
                   "button1":button1,
                   "data":data,
                   "category1":category,
                   "category2": category2,
                   "category3": category3,
                   "designs": designs,

                   }

        return render(request,"illust/index.html",context)


index   = illustView.as_view()



#LoginRequiredMixinでログイン状態をチェック、認証状態にあればアクセスを許可する。
class uploadView(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):


        return render(request, "illust/upload.html")

    def post(self, request, *args, **kwargs):


        if "file" not in request.FILES:
            return redirect("illust:index")

        mime_type = magic.from_buffer(request.FILES["file"].read(1024), mime=True)
        print(mime_type)

        copied          = request.POST.copy()
        copied["mime"]  = mime_type
        copied["user"]  = request.user.id #←ユーザーIDをセットする

        form = DesignForm(copied, request.FILES)

        if form.is_valid():
            print("バリデーションOK ")
            if mime_type in ALLOWED_MIME:
                result  = form.save()
            else:
                print("このファイルは許可されていません")
                return redirect("illust:upload")
        else:
            print("バリデーションNG")
            return redirect("illust:upload")

        return redirect("illust:upload")

upload  = uploadView.as_view()
