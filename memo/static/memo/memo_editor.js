
Ext.onReady(function() {

Ext.QuickTips.init();

var formstore = new Ext.data.JsonStore({
    storeId: 'store_form',
    remoteSort : true,
    baseParams: {
        param1: window.testparam
    },
    proxy : new Ext.data.HttpProxy({
        method: 'GET',
        prettyUrls: false,
        reader: {
            type: 'json',
            root: 'data'
        },
        api:{
            read: '/memo/data/form/'
        }
    }),
    fields: [
        {name:'header', type: 'string'},
        {name:'is_favorite', type:'boolean'}
        ]
});
//formstore.load();


})