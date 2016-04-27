<template>
    <div class="main-header">
        <nav class="navbar navbar-default navbar-fixed-top">
            <div class="container-fluid">
                <div class="navbar-header pull-left">
                    <a class="navbar-brand" v-link="'/'">weiqi.gs</a>

                    <a href="javascript:void(0)" @click="toggleSidebar()" class="sidebar-toggle">
                        <span class="divider"></span>
                        <span class="toggle"></span>
                        <span class="divider"></span>
                    </a>
                </div>

                <ul class="nav navbar-nav navbar-right pull-right">
                    <li class="dropdown">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                            <i class="fa fa-cog fa-fw"></i>
                        </a>
                        <ul class="dropdown-menu">
                            <template v-if="user.loggedIn">
                                <li>
                                    <a v-link="{name:'user', params:{userID:user.userID}}">
                                       <i class="fa fa-user fa-fw"></i> {{$t('header.profile')}}
                                    </a>
                                </li>

                                <li>
                                    <a v-link="'/settings'">
                                        <i class="fa fa-cog fa-fw"></i> {{$t('header.settings')}}
                                    </a>
                                </li>

                                <li class="divider"></li>
                            </template>

                            <li><a href="#"><i class="fa fa-users fa-fw"></i> Rooms</a></li>
                            <li><a href="#"><i class="fa fa-user-plus fa-fw"></i> Friends</a></li>

                            <li class="divider"></li>

                            <li>
                                <a v-link="'/faq'">
                                    <i class="fa fa-question-circle fa-fw"></i> {{$t('header.help')}}
                                </a>
                            </li>

                            <template v-if="user.loggedIn">
                                <li class="divider"></li>

                                <li>
                                    <a href="/api/auth/logout">
                                        <i class="fa fa-sign-out"></i> {{$t('header.logout')}}
                                    </a>
                                </li>
                            </template>
                        </ul>
                    </li>
                </ul>

                <p class="navbar-text navbar-right pull-right">
                    <qi-connectivity></qi-connectivity>
                </p>
            </div>
        </nav>
    </div>
</template>

<script>
    import { toggleSidebar } from './../vuex/actions';

    export default {
        vuex: {
            getters: {
                user: function(state) { return state.auth.user; }
            },
            actions: {
                toggleSidebar
            }
        },

        components: {
            'qi-connectivity': require('./connectivity.vue')
        }
    }
</script>