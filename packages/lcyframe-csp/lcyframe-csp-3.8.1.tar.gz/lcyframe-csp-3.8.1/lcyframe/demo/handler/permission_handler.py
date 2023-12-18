#!/usr/bin/env python
# -*- coding:utf-8 -*-

from lcyframe import route
from lcyframe import funts
from base import BaseHandler, helper


@route("/permission/groups")
class PermissionGroupsHandler(BaseHandler):

    @helper.admin(1)
    def get(self):
        """
        角色详情

        Request extra query params:
        - group_id # type: int required:True 角色id

        :return:
        :rtype:
        """

        group_mp = self.model.GroupsModel.get_groups_mapping(self.params["content_type"])
        if not group_mp or str(self.params["group_id"]) not in group_mp:
            raise self.api_error.ErrorCommonPermission
        group = group_mp[str(self.params["group_id"])]
        group = self.model.GroupsModel.get_members_count(None, group)[0]
        self.write_success(group)

    @helper.admin(1)
    def post(self):
        """
        新增角色

        Request extra query params:
        - name # type: str required:True 权限名称
        - content_type # type: int required:True 0系统端角色，1业务的角色
        - describes # type: str required:False 角色说明

        :return:
        :rtype:
        """
        name = self.params.pop("name")
        content_type = self.params.pop("content_type")
        try:
            self.model.GroupsModel.create_groups(name, content_type, **self.params)
        except Exception as e:
            raise self.api_error.ErrorCommonPermission(str(e))
        self.write_success()

    @helper.admin(1)
    def put(self):
        """
        修改角色

        Request extra query params:
        - group_id # type: int required:True id
        - name # type: str required:False 权限名称
        - state # type: int required:False 1启用，0禁用
        - describes # type: str required:False 角色说明

        :return:
        :rtype:
        """
        group_id = self.params.pop("group_id")
        group = self.model.GroupsModel.get_data_by_kv(id=group_id)
        if not group:
            raise self.api_error.ErrorNotData
        content_type = group["content_type"]
        try:
            self.model.GroupsModel.update_group(group_id, content_type, **self.params)
        except Exception as e:
            raise self.api_error.ErrorCommonPermission(str(e))
        self.write_success()

    @helper.admin(1)
    def delete(self):
        """
        删除角色

        Request extra query params:
        - group_id # type: int required:True id

        :return:
        :rtype:
        """

        # self.model.GroupsModel.delete(self.params["oid"])
        self.write_success()


@route("/permission/groups/list")
class PermissionGroupsListHandler(BaseHandler):

    @helper.admin(1)
    def get(self):
        """
        角色列表

        Request extra query params:
        - page # type: int required:False 翻页码
        - count # type: int required:False 每页显示条数
        - state # type: int required:False 状态
        - content_type # type: int required:True 0系统端角色，1业务的角色
        - company_id # type: int required:True 指定商户，默认所有角色。

        :return:
        :rtype:
        """

        count = self.params.get("count", 10)
        page = self.params.get("page", 1)

        sql_and = {}
        orderby = {
            "id": -1
        }
        if self.params.get("content_type"):
            sql_and["content_type"] = self.params["content_type"]
        if self.params.get("state"):
            sql_and["state"] = self.params["state"]
        if self.params.get("company_id"):
            sql_and["company_id"] = self.params["company_id"]

        datas, counts = self.model.GroupsModel.get_group_list_by_page(
            page, count,
            sql_and=sql_and,
            orderby=orderby)

        datas = self.model.GroupsModel.get_members_count(self.params.get("company_id"), *datas)

        self.write_pagination(datas, counts)


@route("/permission/groups/members")
class PermissionGroupsMembersHandler(BaseHandler):

    @helper.admin(1)
    def get(self):
        """
        角色的成员
        查看指定角色或指定商户的成员列表
        :return:
        :rtype:
        """
        company_id = self.params.pop("company_id", None)
        group = self.model.GroupsModel.get_data_by_kv(id=self.params["group_id"])
        datas = self.model.GroupsModel.get_members(company_id, group)
        company_mp = self.model.CompanyModel.get_batch_by_in("name", id=[data["company_id"] for data in datas])
        for data in datas:
            data["company_name"] = company_mp[data["company_id"]]["name"]
        self.write_success({"datas": datas})

    @helper.admin(1)
    def post(self):
        """
        该角色分配成员
        """
        user_ids = list(map(int, self.params["user_id"].split(",")))
        company_id = self.params.pop("company_id")
        group_id = self.params.pop("group_id")
        group = self.model.GroupsModel.get_data_by_kv(id=group_id)
        if not group:
            raise self.api_error.ErrorCommonPermission("角色不存在")

        user_mp = self.model.AdminModel.get_batch_by_in("id", "group_id", "company_id", id=user_ids)
        for id, user in user_mp.items():
            if user["company_id"] == 1 and group["content_type"] == 1:
                raise self.api_error.ErrorCommonPermission("该角色只适用业务端")
            if user["company_id"] > 1 and group["content_type"] == 0:
                raise self.api_error.ErrorCommonPermission("该角色只适用系统端")
            if user["company_id"] != company_id:
                raise self.api_error.ErrorCommonPermission("用户%s不属于该商户" % user["username"])
            # 支持多个角色
            # group_ids = set(user["group_id"].split(","))
            # group_ids.add(str(group_id))
            # group_ids = group_ids-set([0, "0"])
            # self.model.AdminModel.update_data(user["id"], group_id=",".join(list(group_ids)))
            self.model.AdminModel.update_data(user["id"], group_id=str(group_id))
        self.write_success()


@route("/permission/groups/check")
class PermissionGroupsCheckHandler(BaseHandler):

    @helper.admin(1)
    def post(self):
        """
        编辑角色权限
        权限勾选或取消,修改成功后，建议刷新本地权限缓存

        Request extra query params:
        - group_id # type: int required:True 角色id
        - key # type: str required:True 接口标识符
        - method # type: str required:True 接口方法
        - value # type: int required:True 1勾选，0取消

        :return:
        :rtype:
        """

        group_id = self.params["group_id"]
        key = self.params["key"]
        method = self.params["method"]
        value = self.params["value"]

        self.model.GroupsModel.update_group_permission(group_id, key, method, value)
        self.write_success()


@route("/permission/groups/checks")
class PermissionGroupsCheckSHandler(BaseHandler):

    @helper.admin(1)
    def post(self):
        """
        批量修改权限
        编辑角色权限
        权限勾选或取消,修改成功后，建议刷新本地权限缓存

        Request extra query params:
        - group_id # type: int required:True 角色id

        :return:
        :rtype:
        """

        group_id = self.params["group_id"]
        permissions = self.params["permissions"]
        self.model.GroupsModel.update_group_permissions(group_id, permissions)
        self.write_success()


@route("/permission/groups/company")
class PermissionGroupsCompanyHandler(BaseHandler):

    @helper.admin(1)
    def get(self):
        """
        商户的所有角色
        查看某商户的所有角色，不分页

        Request extra query params:
        - company_id # type: int required:True 商户id

        :return:
        :rtype:
        """
        content_type = self.params["content_type"]
        if content_type:
            if not self.params["company_id"]:
                raise self.api_error.ErrorCommonPermission("需提供商户id")
            company_groups_mp = self.model.CompanyGroupsModel.get_company_groups(content_type)
            groups = company_groups_mp.get(str(self.params["company_id"]), [])
        else:
            groups = self.model.CompanyGroupsModel.get_system_groups()

        groups_mp = self.model.GroupsModel.get_groups_mapping(content_type)

        enable_groups = []
        for index, group_id in enumerate(groups):
            if str(group_id) in groups_mp:
                # 已被禁用的，也显示
                g = groups_mp[str(group_id)]
                # if g["state"] != 1:
                #     continue
                enable_groups.append(g)

        enable_groups = self.model.GroupsModel.get_members_count(self.params["company_id"], *enable_groups)

        self.write_success(data={"datas": enable_groups})

    @helper.admin(1)
    def post(self):
        """
        把角色分配给商户

        Request extra query params:
        - group_id # type: str required:True 角色id， 多个角色用英文逗号隔开
        - company_id # type: int required:True 商户id

        :return:
        :rtype:
        """
        group_id = self.params.pop("group_id", "").split(",")
        company_id = self.params.pop("company_id")
        if company_id == 1:
            raise self.api_error.ErrorCommonPermission("禁止修改系统端角色")
        self.model.CompanyGroupsModel.update_company_group(company_id, group_id)
        self.write_success()

    @helper.admin(1)
    def delete(self):
        """
        移除角色
        将角色从商户下移除，属于该角色的用户将失去该角色的所有权限

        Request extra query params:
        - group_id # type: int required:True 角色id
        - company_id # type: int required:True 商户id

        :return:
        :rtype:
        """

        group_id = self.params.pop("group_id", "").split(",")
        company_id = self.params.pop("company_id")
        self.model.CompanyGroupsModel.remove_company_group(company_id, group_id)
        self.write_success()


@route("/permission")
class PermissionHandler(BaseHandler):

    @helper.admin(1)
    def get(self):
        """
        权限详情

        Request extra query params:
        - permission_id # type: int required:True id

        :return:
        :rtype:
        """

        data = self.model.RBACPermissionModel.get_data_by_kv(id=self.params["permission_id"])

        self.write_success(data)

    @helper.admin(1)
    def post(self):
        """
        新增

        Request extra query params:
        - content_type # type: int required:True 0系统端角色，1业务的角色
        - key # type: str required:True 接口标识符
        - name # type: str required:True 名称
        - permission_class # type: int required:True 类别，tag标签，api接口权限
        - method # type: str required:False 接口方法， 当permission_class=api时必须提供
        - parent_id # type: str required:False 父级id
        - describes # type: str required:False 角色说明
        - state # type: int required:False 角色说明
        - hook_func # type: str required:False 钩子方法

        :return:
        :rtype:
        """
        key = self.params.pop("key")
        name = self.params.pop("name")
        permission_class = self.params.pop("permission_class")
        content_type = self.params.pop("content_type")

        if content_type not in [0, 1]:
            raise self.api_error.ErrorCommonPermission("参数错误")
        if self.model.RBACPermissionModel.get_datas_by_spec(sql_and=dict(key=key)):
            raise self.api_error.ErrorCommonPermission("`%s`已被使用" % key)
        if self.model.RBACPermissionModel.get_datas_by_spec(sql_and=dict(name=name, content_type=content_type)):
            raise self.api_error.ErrorCommonPermission("`%s`已被使用" % name)
        if self.params.get("hook_func") and self.model.RBACPermissionModel.get_datas_by_spec(
                sql_and=dict(hook_func=self.params.get("hook_func"))):
            raise self.api_error.ErrorCommonPermission("`%s`已存在" % self.params.get("hook_func"))
        if permission_class not in ["tag", "api", "logic逻辑权限"]:
            raise self.api_error.ErrorCommonPermission("permission_class只能是tag，api，logic中的一个")
        if permission_class != "tag":
            if not self.params.get("method"):
                raise self.api_error.ErrorCommonPermission("没有提供方法名method")
            for method in self.params.get("method").split(","):
                if method not in ["get", "delete", "put", "post"]:
                    raise self.api_error.ErrorCommonPermission("不支持该方法名" % method)

        self.model.RBACPermissionModel.create_permission(key, name, permission_class, content_type, **self.params)
        self.write_success()

    @helper.admin(1)
    def put(self):
        """
        修改
        修改权限名称，描述，状态，钩子

        Request extra query params:
        - content_type # type: int required:True 0系统端角色，1业务的角色
        - key # type: str required:False 接口标识符
        - name # type: str required:False 名称
        - permission_class # type: int required:False 类别，tag标签，api接口权限
        - method # type: str required:False 接口方法， 当permission_class=api时必须提供
        - parent_id # type: int required:False 父级id
        - describes # type: str required:False 角色说明
        - state # type: int required:False 角色说明
        - hook_func # type: str required:False 钩子方法

        :return:
        :rtype:
        """

        permission_id = self.params.pop("permission_id")
        content_type = self.params.pop("content_type")
        permission = self.model.RBACPermissionModel.get_data_by_kv(id=permission_id)
        if not permission:
            raise self.api_error.ErrorCommonPermission
        if self.params.get("parent_id") and self.params["parent_id"] == permission_id:
            raise self.api_error.ErrorCommonPermission("父级id错误")

        # 提交0，代表不设置父级id
        if "parent_id" in self.params and self.params["parent_id"] == 0:
            self.params["parent_id"] = None
        self.model.RBACPermissionModel.update_permission(permission_id, content_type, **self.params)
        self.write_success()

    @helper.admin(1)
    def delete(self):
        """
        删除

        Request extra query params:
        - permission_id # type: int required:True id

        :return:
        :rtype:
        """
        permission_id = self.params.pop("permission_id")
        content_type = self.params.pop("content_type")
        self.model.RBACPermissionModel.remove_permission(permission_id, content_type)
        self.write_success()


@route("/permission/list")
class PermissionListHandler(BaseHandler):

    @helper.admin(1)
    def get(self):
        """
        权限条目清单

        Request extra query params:
        - state # type: int required:False 状态
        - content_type # type: int required:True 0系统端权限条目，1业务端权限条目

        :return:
        :rtype:
        """
        permissions = []
        for item in self.model.RBACPermissionModel.get_permissions_list(self.params["content_type"]):
            if item["state"] == 1:
                permissions.append(item)

        self.write_success({"datas": permissions})


@route("/permission/tags/list")
class PermissionTagsListHandler(BaseHandler):

    @helper.admin(1)
    def get(self):
        """
        查看权限列表

        Request extra query params:
        - content_type # type: int required:True 0系统端权限条目，1业务端权限条目

        :return:
        :rtype:
        """
        page, count = self.params.get("page", 1), self.params.get("count", 10)
        sql_and = {
            "permission_class": self.params["permission_class"]
        }
        orderby = {
            "id": -1
        }
        if self.params.get("name"):
            sql_and["name"] = {"REGEXP": self.params.get("name")}
        if self.params.get("content_type") != None:
            sql_and["content_type"] = self.params.get("content_type")

        datas, counts = self.model.RBACPermissionModel.get_list_by_page(
            page, count,
            sql_and=sql_and,
            orderby=orderby)

        permissions_mp = self.model.RBACPermissionModel.get_batch_by_in("id", "name",
                                                                        id=[d["parent_id"] for d in datas if
                                                                            d["parent_id"]])
        for d in datas:
            if d["parent_id"] in permissions_mp:
                d["parent_name"] = permissions_mp[d["parent_id"]]["name"]

        self.write_pagination(datas, counts)


@route("/permission/tags")
class PermissionTagsHandler(BaseHandler):

    @helper.admin(1)
    def get(self):
        """
        查看权限类别(下拉)

        Request extra query params:
        - content_type # type: int required:True 0系统端权限条目，1业务端权限条目

        :return:
        :rtype:
        """
        permissions_tags = []
        datas = self.model.RBACPermissionModel.get_permissions_list(self.params["content_type"])

        def col_tags(permissions):
            for item in permissions:
                if item["permission_class"] == "tag":
                    permissions_tags.append(item)

                if item.get("children"):
                    col_tags(item["children"])

        col_tags(datas)

        self.write_success({"datas": permissions_tags})


@route("/permission/enable")
class PermissionEnableHandler(BaseHandler):

    @helper.admin(1)
    def get(self):
        """
        是否启用权限系统

        :return:
        :rtype:
        """
        data = self.model.RBACPermissionModel.is_enable(self.params["content_type"])
        self.write_success(data={
            "enable": 1 if data else 0
        })

    @helper.admin(1)
    def post(self):
        """
        启用停用
        停用权限系统后，所有访问都不做拦截

        Request extra query params:
        - state # type: int required:True 状态， 1启用，0停用

        :return:
        :rtype:
        """
        state = self.params.pop("state")
        if state:
            self.model.RBACPermissionModel.enable_permission(self.params["content_type"])
        else:
            self.model.RBACPermissionModel.disable_permission(self.params["content_type"])
        self.write_success()


@route("/permission/loads")
class PermissionLoadseHandler(BaseHandler):

    @helper.admin(1)
    def post(self):
        """
        收集并导入当前所有handler的权限条目
        当后端新增新的api逻辑后，调用该方法可自动载入新增的权限条目。该功能仅支持系统端
        Request extra query params:
        - state # type: int required:True 状态， 1启用，0停用

        :return:
        :rtype:
        """
        new_permission = {}

        routes = {}
        routes_hander_mp = {}
        exists_permission = {}
        for item in self.application.handlers:
            key = item.name
            if key in ["DocsHandler", "BaseHandler"]:
                continue
            routes_hander_mp[key] = item.handler_class
            funcs = vars(item.target).keys()
            routes.setdefault(key, [])
            for method in ["get", "post", "put", "delete"]:
                if method in funcs:
                    routes[key].append(method)
                else:
                    continue

        # 已存在的权限
        permissions = self.model.RBACPermissionModel.get_datas_by_spec(sql_and={"content_type": 0})
        for permission in permissions:
            exists_permission[permission["key"]] = permission["method"]

        # 筛选出未导入的选线条目
        for key, methods in routes.items():
            if not methods:
                continue
            if key not in exists_permission:
                new_permission[key] = methods
            else:
                for method in exists_permission[key].split(","):
                    if key in new_permission and method in new_permission[key]:
                        new_permission[key].remove(method)

        datas = self.model.RBACPermissionModel.autoload_permission(routes_hander_mp, new_permission)
        self.write_success({"datas": datas})


@route("/permission/export_and_import")
class PermissionExportImportHandler(BaseHandler):

    @helper.admin(1)
    def get(self):
        """
        导出权限条目
        Request extra query params:
        - state # type: int required:True 状态， 1启用，0停用

        :return:
        :rtype:
        """
        permissions = self.model.RBACPermissionModel.export_permission(self.params["content_type"])
        self.write_success({"datas": permissions})

    @helper.admin(1)
    def post(self):
        """
        上传并导入权限
        file：文件导入，文件格式必须为json形式数组
        permissions：参数提交，json形式数组
        注意：已存在的key不会被导入
        """
        is_delete = self.params.get("is_delete", False)
        content_type = self.params["content_type"]
        permissions = self.params.get("permissions", None)
        file = self.params.get("file", None)
        permissions = permissions or self.utils.to_python(file["body"].decode())
        try:
            data = self.model.RBACPermissionModel.import_permissions(permissions, content_type, is_delete)
        except Exception as e:
            raise self.api_error.ErrorCommonPermission(str(e))

        self.write_success("权限导入完成，成功导入:%s条" % (len(data)))