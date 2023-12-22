# logicore-django-react-pages

[PRG](https://en.wikipedia.org/wiki/Post/Redirect/Get)-like approach for React + Django AJAX apps

Use together with: [React counterpart](https://github.com/Logicore-project/logicore-react-pages)

and on top of: [Running React and Django on a single port](https://github.com/Logicore-project/logicore-django-react)

### Usage

1. Perform: https://github.com/Logicore-project/logicore-django-react#usage-from-scratch-starting-a-django--react-project-for-development

2. Assuming your main apps' name is `main`

3. Add to `views.py` (as an example):

```python
from logicore_django_react_pages.views import ApiView

class HomeView(ApiView):
    url_name = "home"
    url_path = "/"
    WRAPPER = "MainWrapper"
    TEMPLATE = "HomeView"
    title = "Home"

    def get_data(self, request, *args, **kwargs):
        return {"name": "World"} 
```

4. Add to `urls.py`
```python
from logicore_django_react.urls import react_reload_and_static_urls, react_html_template_urls
from main import views # required to register subclasses for ApiView
from logicore_django_react_pages.views import all_api_urls

urlpatterns = [
    # ...
    *all_api_urls(), # in any position
    # ...
]

# add static/media endpoints here if needed
# urlpatterns += static(...)

# lastly, combine with logicore_django_react urls
urlpatterns = react_reload_and_static_urls + urlpatterns + react_html_template_urls
```

5. Install & configure ReactJS counterpart: https://github.com/Logicore-project/logicore-react-pages#installation
