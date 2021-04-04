
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from core.views import login_user, SignupView
from core.api import UserAPIViewSet, EnquiryAPIViewSet, BookmarkAPIViewSet, MainEnquiryAPIViewSet, ContactsAPIViewSet, ImagesAPIViewSet, PropertiesAPIViewSet, FeaturedPropertiesAPIViewSet, InvestPropertiesAPIViewSet, FeaturesAPIViewSet
from core import views as coreviews
from rest_framework.routers import DefaultRouter
from core.views import GoogleLogin

from blog.views import BlogPostAPIViewSet, CategoriesAPIViewSet, BlogPostCommentAPIViewSet

router = DefaultRouter()
router.register('user', UserAPIViewSet, basename='user')

router.register('features', FeaturesAPIViewSet, basename='features-detail')
router.register('properties', PropertiesAPIViewSet, basename='property-detail')
router.register('featured_properties', FeaturedPropertiesAPIViewSet, basename='featuredproperty-detail')
router.register('invest_properties', InvestPropertiesAPIViewSet, basename='investproperties-detail')

router.register('enquiry', EnquiryAPIViewSet, basename='userprofile')
router.register('bookmark', BookmarkAPIViewSet, basename='bookmark')
router.register('main-enquiry', MainEnquiryAPIViewSet, basename='main-enquiry')
router.register('contact', ContactsAPIViewSet, basename='contact')
router.register('images', ImagesAPIViewSet, basename='images')
# router.register('property', CategoriesAPIViewSet, basename='blog-category')

router.register('blog-categories', CategoriesAPIViewSet, basename='categories-detail')
router.register('blog-posts', BlogPostAPIViewSet, basename='post-detail')
router.register('post-comments', BlogPostCommentAPIViewSet, basename='comment-detail')

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls), name='api'),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('rest-auth/google/', GoogleLogin.as_view(), name='google_login'),

    path('admin/', admin.site.urls),
    path('accounts/signup/', SignupView, name='account_signup'),
    path('accounts/login/', login_user, name='account_login'),
    path('accounts/', include('allauth.urls')),

    path('', include('core.urls', namespace='core')),
    path('leadgrow/', include('leadgrow.urls', namespace='leadgrow')),
    path('feawa/', include('feawa.urls', namespace='feawa')),
    path('blog/', include('blog.urls', namespace='blog')),

]

urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)