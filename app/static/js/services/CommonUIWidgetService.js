var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('CommonUIWidgetService',
    ['$modal',
    function (
        $modal){

        var _progressBarSpinnerModalInstance = null;

        var openProgressBarSpinnerModal = function() {
            if (!_progressBarSpinnerModalInstance) {
                _progressBarSpinnerModalInstance= $modal.open({
                  templateUrl: '/static/partials/common/modal_progress_bar_spinner.html',
                  controller: function() {},
                  backdrop: 'static',
                  size: 'md'
                });
            }
        };

        var closeProgressBarSpinnerModal = function() {
            if (_progressBarSpinnerModalInstance) {
                _progressBarSpinnerModalInstance.dismiss();
                _progressBarSpinnerModalInstance = null;
            }
        };

        return {

            openProgressBarSpinnerModal: openProgressBarSpinnerModal,
            closeProgressBarSpinnerModal: closeProgressBarSpinnerModal

        };
    }
]);
