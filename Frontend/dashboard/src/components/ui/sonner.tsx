
import { useTheme } from "next-themes"
import { Toaster as Sonner, toast } from "sonner"

type ToasterProps = React.ComponentProps<typeof Sonner>

const Toaster = ({ ...props }: ToasterProps) => {
  const { theme = "system" } = useTheme()

  return (
    <Sonner
      theme={theme as ToasterProps["theme"]}
      className="toaster group"
      position="top-center"
      toastOptions={{
        classNames: {
          toast:
            "group toast group-[.toaster]:bg-background group-[.toaster]:text-foreground group-[.toaster]:border-border group-[.toaster]:shadow-lg group-[.toaster]:rounded-xl",
          description: "group-[.toast]:text-muted-foreground",
          actionButton:
            "group-[.toast]:bg-primary group-[.toast]:text-primary-foreground",
          cancelButton:
            "group-[.toast]:bg-muted group-[.toast]:text-muted-foreground",
          success: "group-[.toast]:bg-green-500/10 group-[.toast]:border-green-500/20 group-[.toast]:text-green-600 dark:group-[.toast]:text-green-400",
          error: "group-[.toast]:bg-red-500/10 group-[.toast]:border-red-500/20 group-[.toast]:text-red-600 dark:group-[.toast]:text-red-400",
          info: "group-[.toast]:bg-blue-500/10 group-[.toast]:border-blue-500/20 group-[.toast]:text-blue-600 dark:group-[.toast]:text-blue-400",
          warning: "group-[.toast]:bg-yellow-500/10 group-[.toast]:border-yellow-500/20 group-[.toast]:text-yellow-600 dark:group-[.toast]:text-yellow-400",
        },
      }}
      {...props}
    />
  )
}

export { Toaster, toast }
