"use strict";
(self["webpackChunkjupyterlab_keycloak_opener"] = self["webpackChunkjupyterlab_keycloak_opener"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);



const PALETTE_CATEGORY = 'Admin tools';
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.createNew = 'jupyterlab-keycloak-opener:open-keycloak-console';
})(CommandIDs || (CommandIDs = {}));
/**
 * Initialization data for the jupyterlab-keycloak-opener extension.
 */
const plugin = {
    id: 'jupyterlab-keycloak-opener:plugin',
    description: 'A JupyterLab extension.',
    autoStart: true,
    optional: [_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1__.ILauncher, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ICommandPalette],
    activate: (app, launcher, palette) => {
        console.log('JupyterLab extension jupyterlab-keycloak-opener is activated!');
        const { commands } = app;
        const command = CommandIDs.createNew;
        commands.addCommand(command, {
            label: 'Users',
            caption: 'Users',
            icon: args => (args['isPalette'] ? undefined : _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.usersIcon),
            execute: async (args) => {
                window.open('https://auth.opensciencestudio.com/admin/Navteca/console', '_blank', 'noreferrer');
            }
        });
        if (launcher) {
            launcher.add({
                command,
                category: 'Admin tools',
                rank: 1
            });
        }
        if (palette) {
            palette.addItem({
                command,
                args: { isPalette: true },
                category: PALETTE_CATEGORY
            });
        }
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.6370cbd13d8583f2fd1c.js.map