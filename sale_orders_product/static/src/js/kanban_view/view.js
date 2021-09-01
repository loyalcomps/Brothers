odoo.define('sale_orders_product.ProductKanbanView', function (require) {
"use strict";

const KanbanView = require('web.KanbanView');
const KanbanModel = require('sale_orders_product.ProductKanbanModel');
const viewRegistry = require('web.view_registry');

const ProductKanbanView = KanbanView.extend({
    config: _.extend({}, KanbanView.prototype.config, {
        Model: KanbanModel,
    }),
});

viewRegistry.add('fsm_product_kanban', ProductKanbanView);

});
