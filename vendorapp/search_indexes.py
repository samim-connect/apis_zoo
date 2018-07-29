
from haystack import indexes
from .models import Product


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    category = indexes.CharField(model_attr='category', null=True)
    location = indexes.EdgeNgramField(model_attr='location', null=True)

    def get_model(self):
        return Product
