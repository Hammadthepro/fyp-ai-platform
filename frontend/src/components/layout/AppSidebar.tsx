import { Link, useRouterState } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import {
  BellRing,
  BookOpen,
  Calendar as CalendarIcon,
  ClipboardList,
  FileText,
  FolderKanban,
  Home,
  Layers,
  LogOut,
  MessageSquare,
  Settings,
  Sparkles,
  Target,
  Users,
} from "lucide-react";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import { Badge } from "@/components/ui/badge";
import { useAuth } from "@/contexts/AuthContext";
import { notificationsService } from "@/services/notifications.service";
import type { UserRole } from "@/types/api";

interface NavItem {
  title: string;
  to: string;
  icon: typeof Home;
  roles?: UserRole[];
}

const NAV: NavItem[] = [
  { title: "Dashboard", to: "/dashboard", icon: Home },
  { title: "Ideas", to: "/ideas", icon: BookOpen },
  { title: "Groups", to: "/groups", icon: Users },
  { title: "Proposals", to: "/proposals", icon: FileText },
  { title: "Milestones", to: "/milestones", icon: Target },
  { title: "Submissions", to: "/submissions", icon: ClipboardList },
  { title: "Calendar", to: "/calendar", icon: CalendarIcon },
  { title: "Team Chat", to: "/chat", icon: MessageSquare },
  { title: "AI Studio", to: "/ai", icon: Sparkles },
  { title: "Notifications", to: "/notifications", icon: BellRing },
  { title: "Master Data", to: "/master", icon: Layers, roles: ["admin", "professor"] },
  { title: "Admin", to: "/admin", icon: FolderKanban, roles: ["admin"] },
];

export function AppSidebar() {
  const { user, role, logout } = useAuth();
  const pathname = useRouterState({ select: (r) => r.location.pathname });

  const items = NAV.filter((i) => !i.roles || (role && i.roles.includes(role)));

  const { data: unread } = useQuery({
    queryKey: ["notifications", "unread"],
    queryFn: notificationsService.unread,
    refetchInterval: 30000,
    enabled: !!role,
  });
  const unreadCount = unread?.length ?? 0;

  return (
    <Sidebar collapsible="icon">
      <SidebarHeader>
        <div className="flex items-center gap-2 px-2 py-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-md bg-gradient-to-br from-indigo-500 to-purple-600 text-white shadow-sm">
            <Sparkles className="h-4 w-4" />
          </div>
          <div className="flex min-w-0 flex-col">
            <span className="truncate text-sm font-semibold">FYP Platform</span>
            <span className="truncate text-xs capitalize text-muted-foreground">{role ?? "guest"}</span>
          </div>
        </div>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Workspace</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {items.map((item) => {
                const active = pathname === item.to || pathname.startsWith(item.to + "/");
                const showBadge = item.to === "/notifications" && unreadCount > 0;
                return (
                  <SidebarMenuItem key={item.to}>
                    <SidebarMenuButton asChild isActive={active} tooltip={item.title}>
                      <Link to={item.to} className="flex items-center gap-2">
                        <item.icon className="h-4 w-4" />
                        <span className="flex-1">{item.title}</span>
                        {showBadge && (
                          <Badge variant="secondary" className="h-5 min-w-5 justify-center px-1.5 text-[10px]">
                            {unreadCount}
                          </Badge>
                        )}
                      </Link>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                );
              })}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton asChild tooltip="Profile">
              <Link to="/profile" className="flex items-center gap-2">
                <Settings className="h-4 w-4" />
                <span className="truncate">{user?.full_name ?? "Profile"}</span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
          <SidebarMenuItem>
            <SidebarMenuButton onClick={logout} tooltip="Sign out">
              <LogOut className="h-4 w-4" />
              <span>Sign out</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  );
}
