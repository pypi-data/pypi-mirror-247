import os

import pandas as pd
import pytest
from sklearn.datasets import make_classification
from sklearn.exceptions import NotFittedError

os.environ["SAM_ML_LOG_LEVEL"] = "debug"
from sam_ml.models import create_pipeline
from sam_ml.models.classifier import (
    ABC,
    BC,
    BNB,
    DTC,
    ETC,
    GBM,
    GNB,
    GPC,
    KNC,
    LDA,
    LR,
    LSVC,
    MLPC,
    QDA,
    RFC,
    SVC,
    XGBC,
)
from sam_ml.models.main_model import SMAC_INSTALLED


def get_models() -> list:
    return [ABC(), BC(), BNB(), DTC(), ETC(), GNB(), GPC(), GBM(), KNC(), LDA(), LSVC(), LR(), MLPC(), QDA(), RFC(), SVC(), XGBC()]

X, Y = make_classification(n_samples = 50,
                            n_features = 5,
                            n_informative = 5,
                            n_redundant = 0,
                            n_classes = 3,
                            weights = [.2, .3, .8],
                            random_state=42)
X = pd.DataFrame(X, columns=["col1", "col2", "col3", "col4", "col5"])
Y = pd.Series(Y)

X_binary, Y_binary = make_classification(n_samples = 50,
                            n_features = 5,
                            n_informative = 5,
                            n_redundant = 0,
                            n_classes = 2,
                            weights = [.2, .3],
                            random_state=42)
X_binary = pd.DataFrame(X_binary, columns=["col1", "col2", "col3", "col4", "col5"])
Y_binary = pd.Series(Y_binary)


def test_classifier_fit_evaluate_proba_error():
    for classifier in get_models():
        model = create_pipeline(model=classifier, model_name=classifier.model_name)
        model.fit(X, Y)
        with pytest.raises(ValueError): # should raise ValueError if Y is not binary
            model.evaluate_score_proba(X, Y)
            model.evaluate_proba(X, Y, console_out=False)

def test_classifier_fit_evaluate_proba():
    for classifier in get_models():
        model = create_pipeline(model=classifier, model_name=classifier.model_name)
        model.fit(X_binary, Y_binary)
        if model.model_type in ("LSVC", "SVC"):
            with pytest.raises(NotImplementedError):
                model.evaluate_score_proba(X_binary, Y_binary)
                model.evaluate_proba(X_binary, Y_binary, console_out=False)
        else:
            model.evaluate_score_proba(X_binary, Y_binary)
            model.evaluate_proba(X_binary, Y_binary, console_out=False)

def test_evaluate_score_error():
    with pytest.raises(NotFittedError):
        for classifier in get_models():
            model = create_pipeline(model=classifier, model_name=classifier.model_name)
            model.evaluate_score(X, Y)

def test_evaluate_score():
    for classifier in get_models():
        model = create_pipeline(model=classifier, model_name=classifier.model_name)
        model.train(X, Y)
        model.evaluate_score(X, Y)

def test_pipelines_train_warm_start():
    for classifier in get_models():
        model = create_pipeline(model=classifier, model_name=classifier.model_name)
        assert model._data_classes_trained == False, "should be False with no training"
        model.train_warm_start(X, Y, console_out=False)
        assert model._data_classes_trained == True, "should be True after first training"
        model.train_warm_start(X, Y, console_out=False)
        assert model._data_classes_trained == True, "should still be True after second training"

def test_pipelines_train_warm_start():
    for classifier in get_models():
        model = create_pipeline(model=classifier, model_name=classifier.model_name)
        assert model._data_classes_trained == False, "should be False with no training"
        model.fit_warm_start(X, Y)
        assert model._data_classes_trained == True, "should be True after first training"
        model.fit_warm_start(X, Y)
        assert model._data_classes_trained == True, "should still be True after second training"

def test_pipelines_train_evaluate():
    for classifier in get_models():
        model = create_pipeline(model=classifier, model_name=classifier.model_name)
        model.train(X, Y, console_out=False)
        model.evaluate(X, Y, console_out=False)
        model.evaluate_score(X, Y)

def test_pipelines_crossvalidation():
    for classifier in get_models():
        model = create_pipeline(model=classifier, model_name=classifier.model_name)
        model.cross_validation(X, Y, cv_num=2)

def test_pipelines_crossvalidation_small_data():
    for classifier in get_models():
        model = create_pipeline(model=classifier, model_name=classifier.model_name)
        model.cross_validation_small_data(X, Y)

def test_pipelines_randomCVsearch():
    for classifier in get_models():
        model = create_pipeline(model=classifier, model_name=classifier.model_name)
        best_param, _ = model.randomCVsearch(X, Y, n_trails=5, cv_num=2)
        assert best_param != {}, "should always find a parameter combination"

def test_pipelines_randomCVsearch_small_data():
    for classifier in get_models():
        model = create_pipeline(model=classifier, model_name=classifier.model_name)
        best_param, _ = model.randomCVsearch(X, Y, n_trails=5, cv_num=2, small_data_eval=True)
        assert best_param != {}, "should always find a parameter combination"

@pytest.mark.with_swig
def test_pipelines_smac_search():
    if SMAC_INSTALLED:
        for classifier in get_models():
            model = create_pipeline(model=classifier, model_name=classifier.model_name)
            best_param = model.smac_search(X, Y, n_trails=5, cv_num=2)
            assert best_param != {}, "should always find a parameter combination"
    else:
        with pytest.raises(ImportError):
            for classifier in get_models():
                model = create_pipeline(model=classifier, model_name=classifier.model_name)
                best_param = model.smac_search(X, Y, n_trails=5, cv_num=2)
                assert best_param != {}, "should always find a parameter combination"

@pytest.mark.with_swig
def test_pipelines_smac_search_small_data():
    if SMAC_INSTALLED:
        for classifier in get_models():
            model = create_pipeline(model=classifier, model_name=classifier.model_name)
            best_param = model.smac_search(X, Y, n_trails=5, cv_num=2, small_data_eval=True)
            assert best_param != {}, "should always find a parameter combination"
    else:
        with pytest.raises(ImportError):
            for classifier in get_models():
                model = create_pipeline(model=classifier, model_name=classifier.model_name)
                best_param = model.smac_search(X, Y, n_trails=5, cv_num=2, small_data_eval=True)
                assert best_param != {}, "should always find a parameter combination"
