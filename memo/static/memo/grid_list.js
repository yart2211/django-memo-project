
Ext.onReady(function() {
Ext.QuickTips.init();
var store = new Ext.data.JsonStore({
    autoDestroy: true,
    autoLoad: true,
    storeId: 'myStore',
    root: 'data',
    remoteSort : true,
    proxy : new Ext.data.HttpProxy({
        method: 'POST',
        prettyUrls: false,
        reader: {
            type: 'json',
            root: 'data'
        },
        api:{
            read: '/memo/data/read/',
            destroy: '/memo/data/destroy/',
        }
    }),
    idProperty: 'name',
    fields: [
        {name:'id', type: 'number'},
        {name:'header', type: 'string'},
        {name:'is_favorite', type:'boolean'},
        {name:'category__name', type:'string'},
        {name:'uuid', type:'string'},
        {name:'date', type:'date',  dateFormat: 'd.m.Y h:i'}],
    sortInfo: {field:'header', direction:'ASC'}
});
    var encode = false;
    var local = false;
    var filters = new Ext.ux.grid.GridFilters({
        encode: encode,
        local: local,
        filters: [{
            type: 'string',
            dataIndex: 'header'
        }, {
            type: 'boolean',
            dataIndex: 'is_favorite'
        }, {
            type: 'string',
            dataIndex: 'category__name'
        }, {
            type: 'date',
            dataIndex: 'date',
        }
        ]
    });

 // Crid. Метаданные зашиты внутри грида
    var grid = new Ext.grid.GridPanel({
        store: store,
        plugins: [filters],
        // inline toolbars
        tbar:[{
            text:'Добавить',
            tooltip:'Добавить новую заметку',
            iconCls:'add-small-icon',
            handler:function(){
                window.location = "/memo/form/new/";
            }
        }],
        columns: [
            {
                xtype: 'actioncolumn',
                width    : 50,
                renderer : function(value, md, record, rowIndex, col, store){
                    var rec = store.getAt(rowIndex);
                    var id = rec.get('uuid')
                    return '<a title="Редактировать" href="form/' + rec.get('id') +'"><div class="memo-edit"></div>' +
                        '</a> <a title="Открыть" href="' + id +'"><div class="memo-card"></div></a>';
                }
            },
            {
                xtype: 'actioncolumn',
                width: 70,
                header: 'Избранные',
                dataIndex: 'is_favorite',
                sortable : true,
                items: [
                    {
                        getClass: function(v, meta, rec) {
                             if (rec.get('is_favorite')){
                                 this.items[0].tooltip = 'Удалить из избранных';
                                 return 'favorite_on'
                             }
                             else{
                                  this.items[0].tooltip = 'Добавить в избранные'
                                 return 'favorite_off'
                             }
                        },
                        handler: function(grid, rowIndex, colIndex, item, e, record, row) {
                            var rec = store.getAt(rowIndex);
                            Ext.Ajax.request({
                               url: '/memo/data/changefavorite/',
                               success: function(response){
                                   res = JSON.parse(response.responseText);
                                   record = store.getAt(rowIndex);
                                   record.set("is_favorite",res.data);
                                   record.commit();
                                   grid.getView().refresh();
                               },
                               failure: function(response, item){
                                   console.log(response);
                               },
                               params: { 'id': rec.get('id') }
                            });
                        }
                    }
                ]
            },
            {
                id       :'header',
                header   : 'Заголовок',
                width    : 150,
                sortable : true,
                filterable: true,
                dataIndex: 'header'
            },
            {
                header   : 'Категория',
                width    : 100,
                sortable : true,
                dataIndex: 'category__name'
            },
            {
                header   : 'Дата создания',
                width    : 100,
                sortable : true,
                dataIndex: 'date',
                renderer : Ext.util.Format.dateRenderer('d.m.Y h:i')
            },
            {
                xtype: 'actioncolumn',
                width: 50,
                //header:'Удаление',
                items: [
                    {
                        getClass: function(v, meta, rec) {
                            this.items[0].tooltip = 'Удалить заметку';
                            return 'memo-delete'
                        },
                        handler: function(grid, rowIndex, colIndex, item, e, record, row) {
                            var rec = store.getAt(rowIndex);
                            Ext.Ajax.request({
                               url: '/memo/data/destroy/',
                               success: function(response){
                                   res = JSON.parse(response.responseText);
                                   grid.store.removeAt(rowIndex);
                                   grid.getView().refresh();
                               },
                               failure: function(response, item){
                                   console.log(response);
                               },
                               params: { 'id': rec.get('id') }
                            });
                        }
                    }
                ]
            },
        ],
        stripeRows: true,
        //autoExpandColumn: 'header',
        height: 350,
        width: '100%',
        title: 'Список заметок',
        stateful: true,
        stateId: 'grid',

        bbar: new Ext.PagingToolbar({
            store: store,
            pageSize: 50,
            plugins: [filters]
        })
    });
        grid.getBottomToolbar().add([
        '->',
           {
               text: 'Сбросить все фильтры',
               handler: function () {
                   grid.filters.clearFilters();
               }
           }
	    ]);

  grid.render('grid_list');

})