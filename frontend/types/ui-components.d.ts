// Type declarations for UI components
declare module '@/components/ui/badge' {
  export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
    variant?: 'default' | 'secondary' | 'destructive' | 'outline' | 'success' | 'warning' | 'info';
  }
  export const Badge: React.FC<BadgeProps>;
  export const badgeVariants: any;
}

declare module '@/components/ui/button' {
  export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: 'default' | 'destructive' | 'outline' | 'secondary' | 'ghost' | 'link';
    size?: 'default' | 'sm' | 'lg' | 'icon';
  }
  export const Button: React.FC<ButtonProps>;
  export const buttonVariants: any;
}

declare module '@/components/ui/card' {
  export const Card: React.FC<React.HTMLAttributes<HTMLDivElement>>;
  export const CardContent: React.FC<React.HTMLAttributes<HTMLDivElement>>;
  export const CardDescription: React.FC<React.HTMLAttributes<HTMLDivElement>>;
  export const CardFooter: React.FC<React.HTMLAttributes<HTMLDivElement>>;
  export const CardHeader: React.FC<React.HTMLAttributes<HTMLDivElement>>;
  export const CardTitle: React.FC<React.HTMLAttributes<HTMLDivElement>>;
}

declare module '@/components/ui/tabs' {
  export interface TabsProps extends React.HTMLAttributes<HTMLDivElement> {
    value?: string;
    onValueChange?: (value: string) => void;
  }
  export interface TabsContentProps extends React.HTMLAttributes<HTMLDivElement> {
    value: string;
  }
  export interface TabsListProps extends React.HTMLAttributes<HTMLDivElement> {}
  export interface TabsTriggerProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    value: string;
  }
  
  export const Tabs: React.FC<TabsProps>;
  export const TabsContent: React.FC<TabsContentProps>;
  export const TabsList: React.FC<TabsListProps>;
  export const TabsTrigger: React.FC<TabsTriggerProps>;
}

declare module '@/components/ui/progress' {
  export interface ProgressProps extends React.HTMLAttributes<HTMLDivElement> {
    value?: number;
  }
  export const Progress: React.FC<ProgressProps>;
}
